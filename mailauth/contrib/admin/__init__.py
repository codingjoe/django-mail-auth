import django

if django.VERSION < (4, 0):
    default_app_config = "mailauth.contrib.admin.apps.MailAuthAdmin"
