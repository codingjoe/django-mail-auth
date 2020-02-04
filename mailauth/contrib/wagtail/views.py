from django.contrib import messages
from django.http import response
from django.utils.translation import gettext_lazy as _
from wagtail.admin.views.account import LoginView as WagtailLoginView

from mailauth.forms import EmailLoginForm

__all__ = ('LoginView',)


class LoginView(WagtailLoginView):
    """Authentication view for Wagtail admin."""

    def get_form_class(self):
        return EmailLoginForm

    def form_valid(self, form):
        form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('We sent you an email with instructions to log into your account.'),
        )
        return response.HttpResponseRedirect(self.get_success_url())
