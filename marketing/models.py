from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_save

from marketing.utils import Mailchimp


class MarketingPreference(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=True)
    mailchimp_subscribed = models.BooleanField(null=True)
    mailchimp_msg = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


def marketing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        response_data = Mailchimp().subscribe(instance.user.email)


post_save.connect(marketing_pref_create_receiver, sender=MarketingPreference)


def make_marketing_pref_receiver(sender, instance, created, *args, **kwargs):
    if created:
        response_data = MarketingPreference.objects.get_or_create(user=instance)


post_save.connect(make_marketing_pref_receiver, sender=settings.AUTH_USER_MODEL)


def maketing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            response_data = Mailchimp().subscribe(instance.user.email)
        else:
            response_data = Mailchimp().unsubscribe(instance.user.email)

        print(response_data['status'])

        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data


pre_save.connect(maketing_pref_update_receiver, sender=MarketingPreference)
