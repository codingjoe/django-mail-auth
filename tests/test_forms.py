import pytest
from django.core import mail

from mailauth.forms import BaseLoginForm, EmailLoginForm


class TestBaseLoginForm:
    def test_save(self):
        with pytest.raises(NotImplementedError):
            BaseLoginForm().save()


class TestEmailLoginForm:
    def test_send_mail__html_template(self):
        class MyEmailLoginForm(EmailLoginForm):
            html_email_template_name = EmailLoginForm.email_template_name

        MyEmailLoginForm(request=None).send_mail('spiderman@avengers.com', {})
        assert mail.outbox[-1].alternatives
