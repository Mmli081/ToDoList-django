from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['id', 'email', 'username', 'is_staff']
    list_filter = ['is_staff', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()