from django.core import mail


class TestAdminLoginView:

    def test_get(self, client):
        response = client.get('/admin/login/')
        assert response.status_code == 200
        assert b'type="email"' in response.content
        assert b'id="id_email"' in response.content

    def test_post(self, client, user, signature):
        response = client.post(
            '/admin/login/',
            data={'email': 'spiderman@avengers.com'}
        )
        assert response.status_code == 302, response.content.decode()
        assert signature in mail.outbox[-1].body

    def test_post__user_does_not_exist(self, db, client):
        response = client.post(
            '/admin/login/',
            data={'email': 'superman@avengers.com'}
        )
        assert response.status_code == 302, response.content.decode()
        assert not mail.outbox
