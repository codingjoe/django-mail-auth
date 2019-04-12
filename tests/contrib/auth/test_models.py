import pytest

from mailauth.contrib.user.models import EmailUser


class TestAbstractEmailUser:
    def test_has_usable_password(self):
        assert not EmailUser().has_usable_password()


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
