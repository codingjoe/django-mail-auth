import logging

from mailauth.backends import MailAuthBackend


class TestMailAuthBackend:
    def test_authenticate(self, db, user, settings, signer, signature):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        backend = MailAuthBackend()
        backend.signer = signer
        user = backend.authenticate(None, token=signature)
        assert user is not None
        assert user.is_authenticated

    def test_authenticate__user_is_not_active(
        self, db, caplog, user, settings, signer, signature
    ):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        backend = MailAuthBackend()
        backend.signer = signer
        user.is_active = False
        user.save(update_fields=["is_active"], force_update=True)
        with caplog.at_level(logging.WARNING):
            user = backend.authenticate(None, token=signature)

        assert user is None
        assert caplog.records[-1].levelname == "WARNING"
        assert caplog.records[-1].message == (
            "User 'spiderman@avengers.com' is not allowed to authenticate."
        )

    def test_authenticate__user_does_not_exist(
        self, db, caplog, settings, signer, signature
    ):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        backend = MailAuthBackend()
        backend.signer = signer
        with caplog.at_level(logging.WARNING):
            user = backend.authenticate(None, token=signature)
        assert user is None
        assert caplog.records[-1].levelname == "WARNING"
        assert caplog.records[-1].message == (
            "Valid token for non-existing user. Maybe the user has been deleted."
        )

    def test_authenticate__timeout(self, db, caplog, user, settings, signer, signature):
        settings.LOGIN_URL_TIMEOUT = 0
        backend = MailAuthBackend()
        backend.signer = signer
        with caplog.at_level(logging.WARNING):
            user = backend.authenticate(None, token=signature)
        assert user is None
        assert caplog.records[-1].levelname == "WARNING"
        assert caplog.records[-1].message == "Token has expired."

    def test_authenticate__corrupted_token(
        self, db, caplog, user, settings, signer, signature
    ):
        settings.LOGIN_URL_TIMEOUT = 0
        backend = MailAuthBackend()
        backend.signer = signer
        with caplog.at_level(logging.ERROR):
            user = backend.authenticate(None, token="not/a/valid-token")
        assert user is None
        assert caplog.records[-1].levelname == "ERROR"
        assert (
            caplog.records[-1].message
            == 'Malicious or corrupted login token received: "not/a/valid-token"'
        )

    def test_get_token(self, signer, signature, user):
        backend = MailAuthBackend()
        MailAuthBackend.signer = signer
        assert backend.get_token(user) == signature

    def test_get_login_url(self, signer, signature):
        backend = MailAuthBackend()
        MailAuthBackend.signer = signer
        assert backend.get_login_url(signature) == (f"/accounts/login/{signature}")
