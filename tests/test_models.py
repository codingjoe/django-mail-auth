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
