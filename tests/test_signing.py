import pytest
from django.contrib.auth import get_user_model
from django.core.signing import SignatureExpired
from django.utils import timezone

from mailauth import signing


class TestUserSigner:
    def test_sign(self, user, signer, signature):
        assert signer.sign(user) == signature

    def test_unsign(self, db, signer, signature):
        user = get_user_model().objects.create_user(
            pk=1337,
            email="spiderman@avengers.com",
            last_login=timezone.datetime(2002, 5, 3, tzinfo=timezone.utc),
        )
        assert user == signer.unsign(signature)

    def test_unsign__no_user(self, db, signer, signature):
        with pytest.raises(
            signing.UserDoesNotExist, match="User with pk=1337 does not exist"
        ):
            signer.unsign(signature)

    def test_unsign__last_login(self, db, signer, signature):
        get_user_model().objects.create_user(
            pk=1337,
            email="spiderman@avengers.com",
            # later date, that does not match the signature
            last_login=timezone.datetime(2012, 7, 3, tzinfo=timezone.utc),
        )
        with pytest.raises(
            SignatureExpired,
            match="The access token for <EmailUser: spiderman@avengers.com> seems used",
        ):
            signer.unsign(signature)

    def test_unsing__single_use(self, db, signer, signature):
        user = get_user_model().objects.create_user(
            pk=1337,
            email="spiderman@avengers.com",
            # later date, that does not match the signature (token was used)
            last_login=timezone.datetime(2012, 7, 3, tzinfo=timezone.utc),
        )
        assert user == signer.unsign(signature, single_use=False)
        # test a second time to make sure token can be used more than one time
        assert user == signer.unsign(signature, single_use=False)
        with pytest.raises(
            SignatureExpired,
            match="The access token for <EmailUser: spiderman@avengers.com> seems used",
        ):
            signer.unsign(signature, single_use=True)

    def test_to_timestamp(self):
        value = timezone.datetime(2002, 5, 3, tzinfo=timezone.utc)
        base62_value = signing.UserSigner.to_timestamp(value=value)
        assert base62_value == "173QUS"

    def test_to_timestamp__empty(self):
        base62_value = signing.UserSigner.to_timestamp(value=None)
        assert base62_value == ""
