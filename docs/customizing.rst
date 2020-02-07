===========
Customizing
===========

Custom login message (like SMS)
_______________________________

Django Mail Auth can be easily extended. Besides template adaptations it is
possible to send different messages like SMS. To make those changes, you
will need to write a custom login form.

Custom login form
-----------------

Custom login forms need to inherit from :class:`.BaseLoginForm` and override
the :meth:`save<.BaseLoginForm.save>` method.

The following example is for a login SMS via twilio. This will require a
custom user model with a unique ``phone_number`` field::

    from django import forms
    from django.contrib.auth import get_user_model
    from django.template import loader
    from mailauth.forms import BaseLoginForm


    class SmsLoginForm(BaseLoginForm):
        phone_number = forms.CharField()

        template_name = 'registration/login_sms.txt
        from_number = None

        def __init__(self, *args, **kwargs):
            self.twilio_client = TwilioRestClient(
                settings.TWILIO_SID,
                settings.TWILIO_AUTH_TOKEN
            )
            super().__init__(*args, **kwargs)

        def save(self):
            phone_number = self.cleaned_data['phone_number']
            user = get_user_model().objects.get(
                phone_number=phone_number
            )
            context = self.get_context(self.request, user)

            from_number = self.from_number or getattr(
                settings, 'DEFAULT_FROM_NUMBER'
            )
            sms_content = loader.render_to_string(
                self.template_name, context
            )

            self.twilio_client.messages.create(
                to=user.phone_number,
                from_=from_number,
                body=sms_content
            )


To add the new login form, simply add a new login view to your URL config with
the custom form::

    from django.urls import path
    from mailauth.views import LoginView

    from .forms import SmsLoginForm

    urlpatterns = [
        path(
            'login/sms/',
            LoginView.as_view(form_class=SmsLoginForm),
            name='login-sms'
        ),
    ]

API documentation
-----------------

.. autoclass:: mailauth.forms.BaseLoginForm
    :members:

Custom User Model
_________________

For convenience, Django Mail Auth provides a
:class:`EmailUser<mailauth.contrib.user.models.EmailUser>` which is almost
identical to Django's built in :class:`User<django.contrib.auth.models.User>`
but without the :attr:`password<django.contrib.auth.models.User.password>`
and :attr:`username<django.contrib.auth.models.User.username>` field.
The :attr:`email<mailauth.contrib.user.models.AbstractEmailUser.email>`
field serves as a username and is – different to Django's User –
unique and case insensitive.

Implementing a custom User model
--------------------------------

.. code-block:: python

    from mailauth.contrib.user.models import AbstractEmailUser
    from phonenumber_field.modelfields import PhoneNumberField


    class SMSUser(AbstractEmailUser):
        phone_number = phone = PhoneNumberField(_("phone number"), unique=True, db_index=True)

    class Meta(AbstractEmailUser.Meta):
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

.. note:: Do not forget to adjust your ``AUTH_USER_MODEL`` to correct ``app_label.ModelName``.

API documentation
-----------------

.. autoclass:: mailauth.contrib.user.models.AbstractEmailUser
    :members:

    .. autoattribute:: mailauth.contrib.user.models.AbstractEmailUser.email
    .. autoattribute:: mailauth.contrib.user.models.AbstractEmailUser.session_salt

.. autoclass:: mailauth.contrib.user.models.EmailUser
    :members:
