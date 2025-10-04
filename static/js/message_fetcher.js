const room_id = window.room_id;
let last_message_id = Number(window.last_message_id) || 0;


async function hitEndpoint() {
    try {
        url = `${window.location.origin}/fetch-messages/?room_id=${room_id}&last_message_id=${last_message_id}`;

        const response = await fetch(url, {
            method: "GET", //
            headers: { "Content-Type": "application/json" }
        });

        const data = await response.json();

        const messages = data.messages;
        window.last_message_id = last_message_id + messages.length;

        messages.forEach(message => {
            const threadsEl = ensureThreadsContainer();
            threadsEl.prepend(createThreadElement(message));
        });

        console.log("Response:", data);

    } catch (error) {
        console.error(`Error hitting endpoint: ${error}"`);
    }
}

setInterval(hitEndpoint, 3000);


function createThreadElement(message) {
    const thread = document.createElement('div');
    thread.className = 'thread';

    const top = document.createElement('div');
    top.className = 'thread__top';

    const author = document.createElement('div');
    author.className = 'thread__author';

    const authorLink = document.createElement('a');
    authorLink.className = 'thread__authorInfo';
    authorLink.href = message.user.profile_url;

    const avatar = document.createElement('div');
    avatar.className = 'avatar avatar--small';

    const img = document.createElement('img');
    img.src = message.user.avatar_url;
    avatar.appendChild(img);

    const uname = document.createElement('span');
    uname.textContent = '@' + message.user.username;

    authorLink.appendChild(avatar);
    authorLink.appendChild(uname);

    const date = document.createElement('span');
    date.className = 'thread__date';
    date.textContent = message.created + ' ago';

    author.appendChild(authorLink);
    author.appendChild(date);
    top.appendChild(author);

    if (message.can_delete && message.delete_url) {
        const delA = document.createElement('a');
        delA.href = message.delete_url;

        const delDiv = document.createElement('div');
        delDiv.className = 'thread__delete';
        delDiv.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32"
           viewBox="0 0 32 32"><title>remove</title>
        <path d="M27.314 6.019l-1.333-1.333-9.98 9.981-9.981-9.981-1.333 1.333 9.981 9.981-9.981 9.98 1.333 1.333 9.981-9.98 9.98 9.98 1.333-1.333-9.98-9.98 9.98-9.981z"></path>
      </svg>
    `;
        delA.appendChild(delDiv);
        top.appendChild(delA);
    }

    const details = document.createElement('div');
    details.className = 'thread__details';
    details.textContent = message.body;

    thread.appendChild(top);
    thread.appendChild(details);

    return thread;
}


function ensureThreadsContainer() {
    let conv = document.querySelector('.room__conversation');

    if (!conv) {
        conv = document.createElement('div');
        conv.className = 'room__conversation';
        document.body.appendChild(conv);
    }

    let threads = conv.querySelector('.threads.scroll');

    if (!threads) {
        threads = document.createElement('div');
        threads.className = 'threads scroll';
        conv.appendChild(threads);
    }
    return threads;
}
