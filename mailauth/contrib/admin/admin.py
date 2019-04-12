from django.contrib import admin

from .views import AdminLoginView

admin.site.login = AdminLoginView.as_view(site=admin.site)
