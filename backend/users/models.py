from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import UniqueConstraint


class User(AbstractUser):
    """ Модель 'Пользователь' """

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты',
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Недопустимый символ в имени пользователя'
        )],
        verbose_name='Уникальный юзернейм',
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    password = models.CharField(
        max_length=128,
        verbose_name='Пароль',
    )
    avatar = models.ImageField(
        upload_to='user_images',
        blank=True,
        null=True,
        verbose_name='Аватар',
    )

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Subscribe(models.Model):
    """ Модель 'Подписчик' """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribing',
        verbose_name='Автор',
    )

    class Meta:
        ordering = ['-id']
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_subscription')
        ]
        verbose_name = 'подписка'
        verbose_name_plural = 'Подписки'
