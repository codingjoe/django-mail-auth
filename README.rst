================
Django Mail Auth
================

|version| |docs| |ci| |coverage| |license|

.. figure:: sample.png
    :width: 425
    :alt: screenshot from a login form

Django Mail Auth is a lightweight authentication backend for Django,
that does not require users to remember passwords.

Django Mail Auth features:

- custom user model support
- drop in Django admin support
- drop in Django User replacement
- drop in Wagtail login replacement
- extendable SMS support

This project was inspired by:

- `Is it time for password-less login?`_ by `Ben Brown`_
- `LOGIN WITHOUT PASSWORD MOST SECURE | WAIT.. WHAT?`_ by `Joris Snoek`_
- `django-nopassword`_ by `Rolf Erik Lekang`_


.. _`Rolf Erik Lekang`: http://rolflekang.com
.. _`django-nopassword`: https://github.com/relekang/django-nopassword
.. _`Is it time for password-less login?`: http://notes.xoxco.com/post/27999787765/is-it-time-for-password-less-login
.. _`LOGIN WITHOUT PASSWORD MOST SECURE | WAIT.. WHAT?`: https://www.lucius.digital/en/blog/login-without-password-most-secure-wait-what
.. _`Ben Brown`: http://twitter.com/benbrown
.. _`Joris Snoek`: https://twitter.com/lucius_digital

Installation
------------

Run this command to install ``django-mail-auth``::

    python3 -m pip install django-mail-auth[wagtail]

Setup
-----

First add ``mailauth`` to you installed apps::

    INSTALLED_APPS = [
        # Django's builtin apps…

        'mailauth',

        'mailauth.contrib.admin',  # optional
        'mailauth.contrib.user',  # optional

        # optional, must be included before "wagtail.admin"
        'mailauth.contrib.wagtail',


        # other apps…
    ]

``mailauth.contrib.admin`` is optional and will replace the admin's login
with token based authentication too.

``mailauth.contrib.user`` is optional and provides a new Django User model.
The new User model needs to be enabled via the ``AUTH_USER_MODEL`` setting::

    # This setting should be either "EmailUser" or
    # any custom subclass of "AbstractEmailUser"
    AUTH_USER_MODEL = 'mailauth_user.EmailUser'

    # optional, Wagtail only
    WAGTAILUSERS_PASSWORD_ENABLED = False


Next you will need to add the new authentication backend::

    AUTHENTICATION_BACKENDS = (
        # default, but now optional
        # This should be removed if you use mailauth.contrib.user or any other
        # custom user model that does not have a username/password
        'django.contrib.auth.backends.ModelBackend',

        # The new access token based authentication backend
        'mailauth.backends.MailAuthBackend',
    )

Django's ``ModelBackend`` is only needed, if you still want to support
password based authentication. If you don't, simply remove it from the list.

Last but not least, go to your URL root config ``urls.py`` and add the following::

    from django.urls import path


    urlpatterns = [
        path('accounts/', include('mailauth.urls')),

        # optional, must be before "wagtail.admin.urls"
        path('', include('mailauth.contrib.wagtail.urls')),
    ]

That's it!

.. note:: Don't forget to setup you Email backend!

.. |version| image:: https://img.shields.io/pypi/v/django-mail-auth.svg
   :target: https://pypi.python.org/pypi/django-mail-auth/
.. |ci| image:: https://travis-ci.com/codingjoe/django-mail-auth.svg?branch=master
   :target: https://travis-ci.com/codingjoe/django-mail-auth
.. |coverage| image:: https://codecov.io/gh/codingjoe/django-mail-auth/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/codingjoe/django-mail-auth
.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: :target: https://raw.githubusercontent.com/codingjoe/django-mail-auth/master/LICENSE
.. |docs| image:: https://readthedocs.org/projects/django-mail-auth/badge/?version=latest
   :target: https://django-mail-auth.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
