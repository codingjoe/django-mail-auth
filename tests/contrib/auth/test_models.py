import pytest
from django.core.exceptions import FieldDoesNotExist

from mailauth.contrib.user.models import EmailUser


class TestAbstractEmailUser:
    def test_has_usable_password(self):
        assert not EmailUser().has_usable_password()

    def test_get_session_auth_hash__default(self, db):
        user = EmailUser(email='spiderman@avengers.com')

        assert user.session_salt
        assert user.get_session_auth_hash()

    def test_get_session_auth_hash__value_error(self, db):
        user = EmailUser(email='spiderman@avengers.com', session_salt=None)

        with pytest.raises(ValueError) as e:
            user.get_session_auth_hash()

        assert "'session_salt' must be set" in str(e.value)

    def test_get_session_auth_hash__unique(self, db):
        spiderman = EmailUser(email='spiderman@avengers.com')
        ironman = EmailUser(email='ironman@avengers.com')

        assert spiderman.get_session_auth_hash() != ironman.get_session_auth_hash()

    def test_password_field(self):
        user = EmailUser(email='spiderman@avengers.com')
        with pytest.raises(FieldDoesNotExist):
            user.password


class TestEmailUserManager:

    def test_create_user(self, db):
        user = EmailUser.objects.create_user('spiderman@avengers.com')
        assert user.pk is not None
        assert user.email == 'spiderman@avengers.com'
        assert not user.is_superuser

    def test_create_superuser(self, db):
        user = EmailUser.objects.create_superuser('spiderman@avengers.com')
        assert user.is_superuser

    def test_create_superuser__no_staff(self, db):
        with pytest.raises(ValueError, match='Superuser must have is_staff=True.'):
            EmailUser.objects.create_superuser(
                'spiderman@avengers.com',
                is_staff=False,
            )

    def test_create_superuser__no_superuser(self, db):
        with pytest.raises(ValueError, match='Superuser must have is_superuser=True.'):
            EmailUser.objects.create_superuser(
                'spiderman@avengers.com',
                is_superuser=False,
            )
