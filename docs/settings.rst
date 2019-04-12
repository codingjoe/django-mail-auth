Settings
========

Mail Auth settings
------------------

.. attribute:: LOGIN_URL_TIMEOUT

    Default: ``900``

    Defines how long a login code is valid in seconds.

.. attribute:: LOGIN_REQUESTED_URL

    Default: ``accounts/login/success``

    Defines the URL the user will be redirected to, after requesting an
    authentication message.

Django related settings
-----------------------

.. attribute:: DEFAULT_FROM_EMAIL

    Default: ``'root@example.com'``

    The sender email address for authentication emails send by Django Mail Auth.

.. attribute:: SECRET_KEY

    .. attention:: *Keep it secret, keep it safe!*

        This key is the foundation of all of Django security measures and for
        this package.
