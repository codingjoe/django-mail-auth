from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.translation import gettext_lazy as _

from . import signals

try:
    from citext import CIEmailField
except ImportError:
    from django.db.models import EmailField as CIEmailField


class EmailUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, **extra_fields):
        """Create and save a user with the given email."""
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, **extra_fields)

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, **extra_fields)


def _get_session_salt():
    return get_random_string(12)


class AbstractEmailUser(AbstractUser):
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    username = None
    password = None

    email = CIEmailField(
        _("email address"), blank=True, null=True, unique=True, db_index=True
    )
    """Unique and case insensitive to serve as a better username."""

    session_salt = models.CharField(
        max_length=12,
        editable=False,
        default=_get_session_salt,
    )
    """Salt for the session hash replacing the password in this function."""

    def has_usable_password(self):
        return False

    objects = EmailUserManager()

    class Meta(AbstractUser.Meta):
        abstract = True
        permissions = [
            ("anonymize", "Can anonymize user"),
        ]

    def get_session_auth_hash(self):
        """Return an HMAC of the :attr:`.session_salt` field."""
        key_salt = "mailauth.contrib.user.models.EmailUserManager.get_session_auth_hash"
        if not self.session_salt:
            raise ValueError("'session_salt' must be set")
        return salted_hmac(key_salt, self.session_salt, algorithm="sha256").hexdigest()

    def anonymize(self, commit=True):
        """
        Anonymize the user data for privacy purposes.

        This method will erase the email address, first and last name.
        You may overwrite this method to add additional fields to anonymize::

            class MyUser(AbstractEmailUser):
                def anonymize(self, commit=True):
                    super().anonymize(commit=False) # do not commit yet
                    self.phone_number = None
                    if commit:
                        self.save()
        """
        signals.anonymize.send(sender=self.__class__, instance=self)
        self.email = None
        self.first_name = ""
        self.last_name = ""
        update_fields = ["email", "first_name", "last_name"]
        if commit:
            self.save(update_fields=update_fields)
        return update_fields


delattr(AbstractEmailUser, "password")


class EmailUser(AbstractEmailUser):
    class Meta(AbstractEmailUser.Meta):
        swappable = "AUTH_USER_MODEL"
