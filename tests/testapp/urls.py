from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('accounts/', include('mailauth.urls')),
    path('admin/', admin.site.urls),
]
