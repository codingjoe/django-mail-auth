import logging

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.core.signing import BadSignature, SignatureExpired
from django.urls import reverse

from . import signing
from .signing import UserDoesNotExist

logger = logging.getLogger(__name__)


class MailAuthBackend(ModelBackend):
    signer = signing.UserSigner()

    def authenticate(self, request, token=None):
        max_age = getattr(settings, 'LOGIN_URL_TIMEOUT', 60 * 15)
        single_use = getattr(settings, 'LOGIN_TOKEN_SINGLE_USE', True)

        try:
            user = self.signer.unsign(token, max_age=max_age, single_use=single_use)
        except UserDoesNotExist:
            logger.warning(
                "Valid token for non-existing user. Maybe the user has been deleted.",
                exc_info=True,
            )
        except SignatureExpired:
            logger.warning("Token has expired.", exc_info=True)
        except BadSignature:
            logger.exception('Malicious or corrupted login token received: "%s"', token)
        else:
            if self.user_can_authenticate(user):
                return user

    @classmethod
    def get_token(cls, user):
        return cls.signer.sign(user)

    @staticmethod
    def get_login_url(token):
        return reverse(
            'mailauth:login-token',
            kwargs={'token': token}
        )
