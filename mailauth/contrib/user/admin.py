from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import (
    gettext_lazy as _,
    ngettext,
)

from . import models


class AnonymizableAdminMixin:
    """
    Mixin for admin classes that provides a `anonymize` action.

    This mixin calls the `anonymize` method of all user model instances.
    """

    actions = ["anonymize"]

    @admin.action(
        permissions=["anonymize"],
        description=_("Anonymize selected %(verbose_name_plural)s"),
    )
    def anonymize(self, request, queryset):
        count = queryset.count()
        for user in queryset.iterator():
            user.anonymize()

        self.message_user(
            request,
            ngettext(
                "%(count)s %(obj_name)s has successfully been anonymized.",
                "%(count)s %(obj_name)s have successfully been anonymized.",
                count,
            )
            % {
                "count": count,
                "obj_name": (
                    self.model._meta.verbose_name_plural
                    if count > 1
                    else self.model._meta.verbose_name
                ),
            },
            fail_silently=True,
        )

    def has_anonymize_permission(self, request, obj=None):
        return request.user.has_perm(f"{self.opts.app_label}.anonymize", obj=obj)


@admin.register(models.EmailUser)
class EmailUserAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    fieldsets = (
        (None, {"fields": (("email", "is_active"), ("first_name", "last_name"))}),
        (
            Group._meta.verbose_name_plural,
            {
                "fields": ("groups",),
            },
        ),
        (
            Permission._meta.verbose_name_plural,
            {
                "classes": ("collapse",),
                "fields": (("is_staff", "is_superuser"), "user_permissions"),
            },
        ),
    )
