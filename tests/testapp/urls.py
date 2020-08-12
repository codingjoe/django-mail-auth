from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('mailauth.urls')),
    path("django-admin/", admin.site.urls),

]

try:
    from wagtail.admin import urls as wagtailadmin_urls
except ImportError:
    pass
else:
    urlpatterns += [
        path("", include("mailauth.contrib.wagtail.urls")),
        path("admin/", include(wagtailadmin_urls)),
    ]
