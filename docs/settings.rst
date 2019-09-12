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

.. attribute:: LOGIN_TOKEN_SINGLE_USE

    Default: ``True``

    Defines if a token can be used more than once.
    If ``True``, the same token can only be used once and will be invalid the next try.
    If ``False``, the same token can be used multiple times and remains valid until expired.

Django related settings
-----------------------

.. attribute:: DEFAULT_FROM_EMAIL

    Default: ``'root@example.com'``

    The sender email address for authentication emails send by Django Mail Auth.

.. attribute:: SECRET_KEY

    .. attention:: *Keep it secret, keep it safe!*

        This key is the foundation of all of Django security measures and for
        this package.
