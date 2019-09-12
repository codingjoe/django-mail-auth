from django.contrib.auth import get_user_model
from django.core import signing
from django.utils import baseconv

__all__ = (
    'UserDoesNotExist', 'UserSigner',
)


class UserDoesNotExist(signing.BadSignature):
    pass


class UserSigner(signing.TimestampSigner):
    """Issue and verify URL safe access tokens for users."""

    @staticmethod
    def to_timestamp(value):
        """
        Return URL safe base62 encoded timestamp of given datetime.

        Args:
            value (datetime.datetime): Datetime instance to encode.

        Returns:
            str: URL safe base62 encoded timestamp.

        """
        if value is None:
            return ''
        return baseconv.base62.encode(int(value.timestamp()))

    def sign(self, user):
        """
        Return access token for given user.

        The access token will not include a expiration date, but a timestamp
        when it has been issued.

        Args:
            user (django.contrib.auth.base_user.AbstractBaseUser):
                User object to issue a token for.

        Returns:
            str: URL safe base64 string.

        """
        return super().sign(value=self._make_hash_value(user))

    def _make_hash_value(self, user):
        last_login = self.to_timestamp(user.last_login)
        user_pk = baseconv.base62.encode(user.pk)
        return self.sep.join((user_pk, last_login))

    def unsign(self, value, max_age=None, single_use=True):
        """
        Verify access token and return user, if the token is valid.

        Args:
            value (str): URL safe base64 encoded access token.
            max_age (datetime.timedelta): Maximum age an access token to be valid.
            single_use (bool):
                If ``True``, the same token can only be used once and will be invalid
                the next try.
                If ``False``, the same token can be used multiple times and remains
                valid until expired.
                Default: ``True``
        Returns:
            django.contrib.user.models.BaseUser: Return user object for given
            access token.

        Raises:
            UserDoesNotExist:
                If user object does not exist in the database. This can happen,
                if the user object has been deleted.
            SignatureExpired:
                If the access token has expired or of the user has been logged in
                after the token has been created. The latter prevents users
                from using tokens multiple times.
            django.core.signing.BadSignature:
                If the signature does not match provided data.

        """
        result = super().unsign(value, max_age=max_age)
        user_pk, last_login = result.rsplit(self.sep, 2)
        user_pk = baseconv.base62.decode(user_pk)
        try:
            user = get_user_model()._default_manager.get(pk=user_pk)
        except get_user_model().DoesNotExist as e:
            raise UserDoesNotExist("User with pk=%s does not exist" % user_pk) from e
        else:
            if (single_use and last_login != '' and
                    self.to_timestamp(user.last_login) != last_login):
                raise signing.SignatureExpired(
                    "The access token for %r seems used" % user
                )
            return user
