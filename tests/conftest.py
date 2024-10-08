import zoneinfo

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from mailauth import signing


class FrozenUserSigner(signing.UserSigner):
    """Freeze timestamp for test runs."""

    def timestamp(self):
        return "1Hjptg"


@pytest.fixture()
def user(db):
    """Return a user instance."""
    return get_user_model().objects.create_user(
        pk=1337,
        email="spiderman@avengers.com",
        last_login=timezone.datetime(2002, 5, 3, tzinfo=zoneinfo.ZoneInfo("UTC")),
    )


@pytest.fixture()
def admin_user(db):
    """Return a user instance."""
    return get_user_model().objects.create_user(
        pk=1337,
        email="spiderman@avengers.com",
        last_login=timezone.datetime(2002, 5, 3, tzinfo=zoneinfo.ZoneInfo("UTC")),
        is_superuser=True,
    )


@pytest.fixture()
def signature():
    """Return a signature matching the user fixture."""
    return "LZ:173QUS:1Hjptg:6oq5DS1NJ7SxJ1o-CpfgaqrImVaRpkcHrzV9yltwcHM"


@pytest.fixture()
def signer():
    """Return a forzen version of the UserSigner."""
    return FrozenUserSigner()
