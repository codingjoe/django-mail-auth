def test_login_view():
    from django.contrib.admin import site

    assert site.login.__module__ == "mailauth.contrib.admin.views"
