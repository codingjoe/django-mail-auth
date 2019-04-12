=========
Templates
=========

There are a couple relevant templates, that can be overridden to your needs.

Mail Auth templates
-------------------

Login templates
~~~~~~~~~~~~~~~

.. attribute:: registration/login_requested.html

This template will be displayed after a user successfully requested a login
URL. This template is not proved by the package and needs to be created.

Email templates
~~~~~~~~~~~~~~~

.. attribute:: registration/login_subject.txt

This template defines the subject line of the email that will be sent to
the user.

This template is provided by the package and can be overridden.

.. attribute:: registration/login_email.txt

This is the plain text template for the email containing the authentication
URL that will be sent to the user.

This template is provided by the package and can be overridden.

.. attribute:: registration/login_email.html

This is the HTML template for the email containing the authentication URL that
will be sent to the user.


This template is optional. If not provided, only plain text emails will be
sent.


Django related templates
------------------------

Mail Auth uses Django's default templates for the login views.

Login templates
~~~~~~~~~~~~~~~

.. attribute:: registration/login.html

This template displays login form, where a user can request a login URL. This
template is not proved Django or by the package and needs to be created.

.. attribute:: registration/logged_out.html

This template will be displayed after a successful logout. This template is
not proved Django or by the package and needs to be created.
