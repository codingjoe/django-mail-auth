from django.dispatch import Signal

anonymize = Signal()
"""
Signal that is emitted when a user and all their data should be anonymized.

Usage::

    from django.dispatch import receiver
    from mailauth.contrib.user.models import EmailUser
    from mailauth.contrib.user.signals import anonymize


    @receiver(anonymize, sender=EmailUser)
    def anonymize_user(sender, instance, update_fields, **kwargs):
        # Do something with related user data
        instance.related_model.delete()

"""
