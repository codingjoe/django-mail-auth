from unittest.mock import Mock

import pytest
from django.contrib import admin
from django.contrib.auth.models import Permission

from mailauth.contrib.user.admin import AnonymizableAdminMixin
from mailauth.contrib.user.models import EmailUser


class TestAnonymizableAdminMixin:
    def test_anonymize__none(self, rf):
        class MyUserModel(EmailUser):
            class Meta:
                app_label = "test"
                verbose_name = "singular"
                verbose_name_plural = "plural"

        class MyModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
            pass

        request = rf.get("/")
        MyModelAdmin(MyUserModel, admin.site).anonymize(
            request, MyUserModel.objects.none()
        )

    @pytest.mark.django_db
    def test_anonymize__one(self, rf, user, monkeypatch):
        class MyModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
            pass

        monkeypatch.setattr(EmailUser, "anonymize", Mock())

        request = rf.get("/")
        MyModelAdmin(type(user), admin.site).anonymize(
            request, type(user).objects.all()
        )
        assert EmailUser.anonymize.was_called_once_with(user)

    @pytest.mark.django_db
    def test_anonymize__many(self, rf, user, monkeypatch):
        class MyModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
            pass

        monkeypatch.setattr(EmailUser, "anonymize", Mock())

        request = rf.get("/")
        MyModelAdmin(type(user), admin.site).anonymize(
            request, type(user).objects.all()
        )
        assert EmailUser.anonymize.was_called_once_with(user)

    def test_has_anonymize_permission(self, rf, user):
        class MyModelAdmin(AnonymizableAdminMixin, admin.ModelAdmin):
            pass

        user.is_staff = True
        user.save()
        request = rf.get("/")
        request.user = user
        assert not MyModelAdmin(type(user), admin.site).has_anonymize_permission(
            request
        )

        permission = Permission.objects.get(
            codename="anonymize",
        )
        user.user_permissions.add(permission)
        del user._perm_cache
        del user._user_perm_cache
        assert MyModelAdmin(type(user), admin.site).has_anonymize_permission(request)
