import pytest
from django.db import IntegrityError

from mailauth.contrib.user import models

try:
    import psycopg2
except ImportError:
    psycopg2 = None


postgres_only = pytest.mark.skipif(
    psycopg2 is None, reason="at least mymodule-1.1 required"
)


class TestEmailUser:
    @postgres_only
    def test_email__ci_unique(self, db):
        models.EmailUser.objects.create_user("IronMan@avengers.com")
        with pytest.raises(IntegrityError):
            models.EmailUser.objects.create_user("ironman@avengers.com")

    @pytest.mark.django_db
    def test_anonymize(self):
        user = models.EmailUser.objects.create_user(
            email="ironman@avengers.com", first_name="Tony", last_name="Stark"
        )
        assert user.anonymize() == ["email", "first_name", "last_name"]
        assert not user.first_name
        assert not user.last_name
        assert not user.email

    def test_anonymize__no_commit(self):
        user = models.EmailUser(
            email="ironman@avengers.com", first_name="Tony", last_name="Stark"
        )
        user.anonymize(commit=False)
        assert not user.first_name
        assert not user.last_name
        assert not user.email
