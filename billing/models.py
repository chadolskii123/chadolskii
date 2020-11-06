from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        obj = None
        created = False
        if user.is_authenticated:
            # Logged in user checkout
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)

        elif guest_email_id is not None:
            # guest user checkout
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            pass
        return obj, created


# Create your models here.
class BillingProfile(models.Model):
    # user = models.ForeignKey(User, unique=True, null=True, blank=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


# def billing_profile_create_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         print("Send to stripe/braintree")
#         instance.customer_id = newID
#         instance.save()


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


# 유저가 만들어 질때 Billing Profile이 생성되게 함
post_save.connect(user_created_receiver, sender=User)
