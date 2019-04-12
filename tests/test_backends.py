from mailauth.backends import MailAuthBackend


class TestMailAuthBackend:

    def test_authenticate(self, db, user, settings, signer, signature):
        settings.LOGIN_URL_TIMEOUT = float('inf')
        backend = MailAuthBackend()
        backend.signer = signer
        user = backend.authenticate(None, token=signature)
        assert user is not None
        assert user.is_authenticated

    def test_authenticate__user_does_not_exist(self, db, settings, signer, signature):
        settings.LOGIN_URL_TIMEOUT = float('inf')
        backend = MailAuthBackend()
        backend.signer = signer
        user = backend.authenticate(None, token=signature)
        assert user is None

    def test_get_token(self, signer, signature, user):
        backend = MailAuthBackend()
        MailAuthBackend.signer = signer
        assert backend.get_token(user) == signature

    def test_get_login_url(self, signer, signature):
        backend = MailAuthBackend()
        MailAuthBackend.signer = signer
        assert backend.get_login_url(signature) == (
            '/accounts/login/LZ/173QUS/1Hjptg/fTLJcaon_7zMDyFTIFtlDqbdSt4'
        )
