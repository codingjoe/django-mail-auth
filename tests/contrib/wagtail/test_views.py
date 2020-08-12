import pytest

from mailauth.forms import EmailLoginForm


class TestLoginView:
    def test_get_from_class(self):
        pytest.importorskip('wagtail')
        from mailauth.contrib.wagtail.views import LoginView
        assert issubclass(LoginView().get_form_class(), EmailLoginForm)

    def test_form_valid(self, rf, db):
        pytest.importorskip('wagtail')
        from mailauth.contrib.wagtail.views import LoginView
        view = LoginView()
        request = rf.get('/')

        class DummyMessageStorage:
            def __init__(self):
                self.messages = []

            def add(self, *args):
                self.messages.append(args)

        msgs = DummyMessageStorage()

        request._messages = msgs
        view.request = request
        form = EmailLoginForm(view.request, data=dict(email='spiderman@avengers.com'))
        assert form.is_valid()
        response = view.form_valid(form)
        assert response.status_code == 302
        assert msgs.messages
