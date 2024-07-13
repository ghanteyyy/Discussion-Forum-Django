from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
    

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=200, null=True, help_text="Введите ваше имя", verbose_name="Имя")
    email = models.EmailField(unique=True, null=True, help_text="Введите ваш email", verbose_name="Email")
    bio = models.TextField(null=True, help_text="Краткая информация о себе", verbose_name="Биография")
    avatar = models.ImageField(null=True, default="avatar.svg", help_text="Загрузите аватар", verbose_name="Аватар")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Topic(models.Model):
    name = models.CharField(max_length=200, help_text="Введите название темы", verbose_name="Тема")

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, help_text="Выберите хоста комнаты", verbose_name="Хост")
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, help_text="Выберите тему для комнаты", verbose_name="Тема")
    name = models.CharField(max_length=200, help_text="Введите название комнаты", verbose_name="Название комнаты")
    description = models.TextField(null=True, blank=True, help_text="Введите описание комнаты", verbose_name="Описание")
    participants = models.ManyToManyField(User, related_name='participants', blank=True, help_text="Выберите участников комнаты", verbose_name="Участники")
    updated = models.DateTimeField(auto_now=True, help_text="Время последнего обновления", verbose_name="Обновлено")
    created = models.DateTimeField(auto_now_add=True, help_text="Время создания комнаты", verbose_name="Создано")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Автор сообщения", verbose_name="Пользователь")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, help_text="Комната, в которой отправлено сообщение", verbose_name="Комната")
    body = models.TextField(help_text="Текст сообщения", verbose_name="Сообщение")
    updated = models.DateTimeField(auto_now=True, help_text="Время последнего обновления сообщения", verbose_name="Обновлено")
    created = models.DateTimeField(auto_now_add=True, help_text="Время создания сообщения", verbose_name="Создано")

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.body[0:50]
