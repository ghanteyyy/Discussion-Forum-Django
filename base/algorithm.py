from __future__ import annotations
import math, re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import timedelta
from typing import Dict, Iterable, List

from django.db.models import Count, Max, Q
from django.utils import timezone

from .models import Message, Room, Topic, User

_WORD_RE = re.compile(r"[A-Za-z0-9']+")


def _tokenize(text: str) -> List[str]:
    return [w.lower() for w in _WORD_RE.findall(text or "")]


def _tf(tokens: List[str]) -> Dict[str, float]:
    c = Counter(tokens); total = sum(c.values()) or 1

    return {k: v / total for k, v in c.items()}


def _idf(docs_tokens: List[List[str]]) -> Dict[str, float]:
    df = Counter(); N = len(docs_tokens) or 1

    for tokens in docs_tokens:
        for t in set(tokens):
            df[t] += 1

    return {t: math.log((N + 1) / (df_t + 1)) + 1.0 for t, df_t in df.items()}


def _tfidf(tokens: List[str], idf: Dict[str, float]) -> Dict[str, float]:
    tf = _tf(tokens)

    return {t: tf[t] * idf.get(t, 0.0) for t in tf}


def _cosine(a: Dict[str, float], b: Dict[str, float]) -> float:
    if not a or not b:
        return 0.0

    dot = sum(wa * b.get(t, 0.0) for t, wa in a.items())
    na = math.sqrt(sum(v*v for v in a.values())) or 1.0
    nb = math.sqrt(sum(v*v for v in b.values())) or 1.0

    return dot / (na * nb)


def _room_text(room: Room, recent_messages: List[str]) -> str:
    return " ".join([
        getattr(room.topic, "name", "") or "",
        room.name or "",
        room.description or "",
        " ".join(recent_messages or []),
    ]).strip()


def _collect_recent_messages(room_ids: Iterable[int], per_room: int = 50):
    msgs = (Message.objects
            .filter(room_id__in=list(room_ids))
            .order_by("room_id", "-created")
            .values("room_id", "body"))

    buckets = defaultdict(list)

    for m in msgs:
        rid = m["room_id"]

        if len(buckets[rid]) < per_room:
            buckets[rid].append(m["body"])

    return buckets

# -------- Algorithm 1: Interest profile + recommendations --------

@dataclass
class Recommendation:
    room: Room
    score: float


def build_user_interest_profile(user: User) -> Dict[str, float]:
    connected = (Room.objects
                 .filter(Q(host_id=user.id) | Q(participants__id=user.id))
                 .select_related("topic").distinct())

    base_text = [
        f"{getattr(r.topic, 'name', '')} {r.name or ''} {r.description or ''}"
        for r in connected
    ]

    user_msgs = list(Message.objects.filter(user_id=user.id)
                     .values_list("body", flat=True))

    tokens = _tokenize(" ".join(base_text + user_msgs))

    # background corpus = all rooms (+ some recent messages)
    all_rooms = Room.objects.select_related("topic").all()[:1000]
    rids = [r.id for r in all_rooms]
    buckets = _collect_recent_messages(rids, per_room=20)
    corpus_tokens = [_tokenize(_room_text(r, buckets.get(r.id, []))) for r in all_rooms]
    idf = _idf(corpus_tokens) if corpus_tokens else {}

    return _tfidf(tokens, idf)


def recommend_rooms_for_user(user: User, limit: int = 10, exclude_joined: bool = True):
    profile = build_user_interest_profile(user)
    if not profile: return []  # no signal yet

    candidates = Room.objects.select_related("topic")
    if exclude_joined:
        candidates = candidates.exclude(Q(host_id=user.id) | Q(participants__id=user.id))
    candidates = candidates.annotate(last_msg=Max("message__created")).distinct()

    rids = [r.id for r in candidates]
    buckets = _collect_recent_messages(rids, per_room=30)
    room_tokens = {r.id: _tokenize(_room_text(r, buckets.get(r.id, []))) for r in candidates}
    idf = _idf(list(room_tokens.values())) if room_tokens else {}

    recs = []

    for r in candidates:
        v = _tfidf(room_tokens[r.id], idf)
        s = _cosine(profile, v)
        if s > 0: recs.append(Recommendation(room=r, score=s))

    recs.sort(key=lambda x: x.score, reverse=True)

    return recs[:limit]

# -------- Algorithm 2: Activity-based trending --------

@dataclass
class ActivityScore:
    room: Room
    score: float

def rank_rooms_by_activity(window_days: int = 7, half_life_hours: float = 48.0, limit: int = 20):
    now = timezone.now()
    since = now - timedelta(days=window_days)

    qs = (Room.objects
          .annotate(
              total_msgs=Count("message"),
              recent_msgs=Count("message", filter=Q(message__created__gte=since)),
              last_activity=Max("message__created"),
          )
          .select_related("topic"))

    ln2 = math.log(2.0)
    scored = []

    for r in qs:
        last = r.last_activity or r.created
        age_h = max((now - last).total_seconds() / 3600.0, 0.0)
        recency = math.exp(-(ln2 * age_h / max(half_life_hours, 1e-6)))

        s = math.log1p(int(r.recent_msgs or 0)) * recency + 0.25 * math.log1p(int(r.total_msgs or 0))
        scored.append(ActivityScore(room=r, score=s))

    scored.sort(key=lambda x: x.score, reverse=True)

    return scored[:limit]
