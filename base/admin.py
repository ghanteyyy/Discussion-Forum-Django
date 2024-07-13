from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, Topic, Room, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name', 'bio', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'name', 'is_staff')
    search_fields = ('email', 'name')
    ordering = ('email',)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name',)}),
    )
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('name', 'host', 'topic', 'description', 'participants')}),
        (_('Dates'), {'fields': ('updated', 'created')}),
    )
    list_display = ('name', 'host', 'topic', 'updated', 'created')
    search_fields = ('name', 'description')
    list_filter = ('topic', 'host')
    filter_horizontal = ('participants',)
    readonly_fields = ('updated', 'created')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {'fields': ('user', 'room', 'body')}),
        (_('Dates'), {'fields': ('updated', 'created')}),
    )
    list_display = ('user', 'room', 'body', 'updated', 'created')
    search_fields = ('user__email', 'body')
    list_filter = ('room', 'user')
    readonly_fields = ('updated', 'created')
