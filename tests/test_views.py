from django.urls import reverse

from mailauth.views import LoginView


class TestLoginView:
    def test_get_initial(self, rf):
        view = LoginView()
        view.request = rf.get("/", data={"next": "foo/bar"})

        assert view.get_initial() == {"next": "foo/bar"}


class TestLoginTokenView:
    def test_get__ok(self, client, user, signature, settings):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        url = reverse("mailauth:login-token", kwargs={"token": signature})
        response = client.get(url)
        assert response.status_code == 302
        assert response.url == "/accounts/profile/"

    def test_get__next(self, client, user, signature, settings):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        url = reverse("mailauth:login-token", kwargs={"token": signature})
        response = client.get(url + "?next=/admin/")
        assert response.status_code == 302
        assert response.url == "/admin/"

    def test_get__invalid_token(self, client, user, signature, settings):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        url = reverse("mailauth:login-token", kwargs={"token": "invalid_token"})
        response = client.get(url)
        assert response.status_code == 403

    def test_get__wrong_signature(self, client, user, signature, settings):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        url = reverse("mailauth:login-token", kwargs={"token": signature + "false"})
        response = client.get(url)
        assert response.status_code == 403

    def test_get__no_user(self, client, signature, settings):
        settings.LOGIN_URL_TIMEOUT = float("inf")
        url = reverse("mailauth:login-token", kwargs={"token": signature})
        response = client.post(url)
        assert response.status_code == 405
