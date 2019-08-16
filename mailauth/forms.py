from django import forms
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db import connection
from django.template import TemplateDoesNotExist, loader
from django.urls import reverse
from django.utils.encoding import iri_to_uri

from mailauth.backends import MailAuthBackend


class BaseLoginForm(forms.Form):
    next = forms.CharField(widget=forms.HiddenInput, required=False)

    def get_login_url(self, request, token, next=None):
        """
        Return user login URL including the access token.

        Args:
            request (django.http.request.HttpRequest): Current request.
            token (str): The user specific authentication token.
            next (str): The path the user should be forwarded to after login.

        Returns:
            str: User login URL including the access token.

        """
        protocol = 'https' if request.is_secure() else 'http'
        current_site = get_current_site(request)
        url = '{protocol}://{domain}{path}'.format(
            protocol=protocol,
            domain=current_site.domain,
            path=reverse(
                'mailauth:login-token',
                kwargs={'token': token}
            )
        )
        if next is not None:
            url += '?next=%s' % iri_to_uri(next)
        return url

    def get_token(self, user):
        """Return the access token."""
        return MailAuthBackend.get_token(user=user)

    def get_context(self, request, user):
        """
        Return the context for a message template render.

        Args:
            request (django.http.request.HttpRequest): Current request.
            user: The user requesting a login message.

        Returns:
            dict:
                A context dictionary including:

                - site
                - site_name
                - token
                - login_url
                - user

        """
        token = self.get_token(user)
        site = get_current_site(request)
        login_url = self.get_login_url(request, token, self.cleaned_data['next'])
        return {
            'site': site,
            'site_name': site.name,
            'token': token,
            'login_url': login_url,
            'user': user,
        }

    def save(self):
        """
        Send login URL to users.

        Called from the login view, if the form is valid.

        This method must be implemented by subclasses. This method
        should trigger the login url to be sent to the user.
        """
        raise NotImplementedError


class EmailLoginForm(BaseLoginForm):
    """Login form that contains only the Users email field."""

    subject_template_name = 'registration/login_subject.txt'
    email_template_name = 'registration/login_email.txt'
    html_email_template_name = 'registration/login_email.html'
    from_email = None

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(EmailLoginForm, self).__init__(*args, **kwargs)

        self.field_name = get_user_model().get_email_field_name()
        model_field = get_user_model()._meta.get_field(self.field_name)
        field = model_field.formfield()
        field.required = True

        self.fields[self.field_name] = field

    def get_users(self, email=None):
        if connection.vendor == 'postgresql':
            query = {self.field_name: email}
        else:
            query = {'%s__iexact' % self.field_name: email}
        return get_user_model()._default_manager.filter(**query).iterator()

    def save(self):
        """
        Generate and send a one-time link for the user to login.

        This method will be called from the view and passed the views request.
        """
        email = self.cleaned_data[self.field_name]
        for user in self.get_users(email):
            context = self.get_context(self.request, user)
            self.send_mail(email, context)

    def send_mail(self, to_email, context):
        """Send a django.core.mail.EmailMultiAlternatives to `to_email`."""
        subject = loader.render_to_string(self.subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(self.email_template_name, context)

        email_message = EmailMultiAlternatives(
            subject, body, self.from_email, [to_email]
        )
        try:
            template = loader.get_template(self.html_email_template_name)
        except TemplateDoesNotExist:
            pass
        else:
            html_email = template.render(context, self.request)
            email_message.attach_alternative(html_email, 'text/html')

        email_message.send()
