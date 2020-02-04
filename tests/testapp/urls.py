from django.contrib import admin
from django.urls import include, path
from wagtail.admin import urls as wagtailadmin_urls

urlpatterns = [
    path('accounts/', include('mailauth.urls')),
    path("", include("mailauth.contrib.wagtail.urls")),
    path("django-admin/", admin.site.urls),
    path("admin/", include(wagtailadmin_urls)),

]
