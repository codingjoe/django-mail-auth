import warnings

import pytest
from django.contrib.auth import get_user_model
from django.core import mail

from mailauth.forms import BaseLoginForm, EmailLoginForm


class TestBaseLoginForm:
    def test_save(self):
        with pytest.raises(NotImplementedError):
            BaseLoginForm().save()


class TestEmailLoginForm:
    def test_get_login_url(self, rf):
        request = rf.get("/")
        form = EmailLoginForm(request=request)
        assert (
            form.get_login_url(request, "TOKEN")
            == "http://testserver/accounts/login/TOKEN"
        )
        assert (
            form.get_login_url(
                request,
                "TOKEN",
                next="/path/?utm_source=website&utm_medium=email#some-anchor",
            )
            == "http://testserver/accounts/login/TOKEN?next=/path/%3Futm_source%3Dwebsite%26utm_medium%3Demail%23some-anchor"
        )

    def test_send_mail__html_template(self):
        class MyEmailLoginForm(EmailLoginForm):
            html_email_template_name = EmailLoginForm.email_template_name

        MyEmailLoginForm(request=None).send_mail("spiderman@avengers.com", {})
        assert mail.outbox[-1].alternatives

    def test_get_users(self, db, user):
        assert list(EmailLoginForm(request=None).get_users("spiderman@avengers.com"))
        assert list(EmailLoginForm(request=None).get_users("SpiderMan@Avengers.com"))
        assert not list(EmailLoginForm(request=None).get_users("SpiderMan@dc.com"))

    def test_get_users__postgres_with_citext(self, monkeypatch):
        class DummyCursor:
            def __enter__(self):
                return self

            def __exit__(self, *args, **kwargs):
                return False

            def execute(self, *args, **kwargs):
                return None

            def fetchone(self):
                return (1,)

        class DummyConnection:
            vendor = "postgresql"
            alias = "with_citext"

            def cursor(self):
                return DummyCursor()

        class DummyQuerySet:
            def iterator(self):
                return iter(())

        captured = {}

        def fake_filter(**kwargs):
            captured.update(kwargs)
            return DummyQuerySet()

        monkeypatch.setattr("mailauth.forms.connection", DummyConnection())
        monkeypatch.setattr(get_user_model()._default_manager, "filter", fake_filter)

        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            list(EmailLoginForm(request=None).get_users("SpiderMan@Avengers.com"))

        assert not warning_list
        assert captured == {"email": "SpiderMan@Avengers.com"}

    def test_get_users__postgres_without_citext(self, monkeypatch):
        class DummyCursor:
            def __enter__(self):
                return self

            def __exit__(self, *args, **kwargs):
                return False

            def execute(self, *args, **kwargs):
                return None

            def fetchone(self):
                return None

        class DummyConnection:
            vendor = "postgresql"
            alias = "without_citext"

            def cursor(self):
                return DummyCursor()

        class DummyQuerySet:
            def iterator(self):
                return iter(())

        captured = {}

        def fake_filter(**kwargs):
            captured.update(kwargs)
            return DummyQuerySet()

        monkeypatch.setattr("mailauth.forms.connection", DummyConnection())
        monkeypatch.setattr(get_user_model()._default_manager, "filter", fake_filter)

        with pytest.warns(RuntimeWarning, match="CITEXT extension not detected"):
            list(EmailLoginForm(request=None).get_users("SpiderMan@Avengers.com"))

        assert captured == {"email__iexact": "SpiderMan@Avengers.com"}
