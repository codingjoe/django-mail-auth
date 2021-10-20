import pytest
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
