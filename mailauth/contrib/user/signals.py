from django.dispatch import Signal

anonymize = Signal()
"""
Signal that is emitted when a user and all their data should be anonymized.

The signal is emitted before the private date is delete on the instance,
thus the receiver can still access the data. The receiver should usually
not alter the instance, but only later related data. We recommend overriding
the anonymize method to modify the instance.

Usage::

    from django.dispatch import receiver
    from mailauth.contrib.user.models import EmailUser
    from mailauth.contrib.user.signals import anonymize


    @receiver(anonymize, sender=EmailUser)
    def anonymize_user(sender, instance, **kwargs):
        # Do something with related user data
        instance.related_model.delete()

"""
