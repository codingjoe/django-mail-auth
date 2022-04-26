from unittest.mock import Mock

import pytest
from django.dispatch import receiver

from mailauth.contrib.user.signals import anonymize


@pytest.mark.django_db
def test_anonymize(user):
    handler = Mock()
    receiver(anonymize, sender=user.__class__)(handler)
    handler.assert_not_called()
    user.anonymize()
    handler.assert_called_once_with(
        signal=anonymize,
        sender=user.__class__,
        instance=user,
    )
