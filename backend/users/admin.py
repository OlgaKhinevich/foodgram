from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import Subscribe, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'avatar',
    )
    search_fields = ('email', 'username')


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
