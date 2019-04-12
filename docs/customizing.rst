===========
Customizing
===========

Django Mail Auth can be easily extend. Besides template adaptations it is
possible to send send different messages like SMS. To make those changes you
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
