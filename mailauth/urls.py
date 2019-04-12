from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from mailauth import views

app_name = 'mailauth'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('login/success/', views.LoginRequestedView.as_view(), name='login-success'),
    re_path('login/(?P<token>.*)$', views.LoginTokenView.as_view(), name='login-token'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
