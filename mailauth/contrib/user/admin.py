from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from . import models


@admin.register(models.EmailUser)
class EmailUserAdmin(admin.ModelAdmin):
    app_label = 'asdf'
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {
            'fields': (('email', 'is_active'), ('first_name', 'last_name'))
        }),
        (Group._meta.verbose_name_plural, {
            'fields': ('groups',),
        }),
        (Permission._meta.verbose_name_plural, {
            'classes': ('collapse',),
            'fields': (('is_staff', 'is_superuser'), 'user_permissions'),
        }),
    )
