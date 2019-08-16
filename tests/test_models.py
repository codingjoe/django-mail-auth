import pytest
from django.db import IntegrityError

from mailauth.contrib.user import models


class TestEmailUser:

    def test_email__ci_unique(self, db):
        models.EmailUser.objects.create_user('IronMan@avengers.com')
        with pytest.raises(IntegrityError):
            models.EmailUser.objects.create_user('ironman@avengers.com')
