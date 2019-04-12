from django.contrib.auth import REDIRECT_FIELD_NAME
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from mailauth.views import LoginView


class AdminLoginView(LoginView):
    template_name = 'mailauth_admin/login.html'
    site = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            **self.site.each_context(self.request),
            'title': _('Log in'),
            'app_path': self.request.get_full_path(),
            'username': self.request.user.get_username(),
        })
        if (REDIRECT_FIELD_NAME not in self.request.GET and
                REDIRECT_FIELD_NAME not in self.request.POST):
            context[REDIRECT_FIELD_NAME] = reverse(
                'admin:index', current_app=self.site.name
            )
        return context
