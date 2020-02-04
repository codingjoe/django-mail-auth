from django.urls import path

from . import views

app_name = 'mailauth_wagtail'

urlpatterns = [
    path('admin/login/', views.LoginView.as_view(), name='wagtailadmin_login'),
]
