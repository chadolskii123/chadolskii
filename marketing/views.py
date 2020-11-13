from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import UpdateView
from django.views.generic.base import View

from marketing.forms import MarketingPreferenceForm
from marketing.mixins import CsrfExemptMixin
from marketing.models import MarketingPreference
from marketing.utils import Mailchimp

MAILCHIMP_EMAIL_LIST_ID = getattr(settings, "MAILCHIMP_EMAIL_LIST_ID", None)


class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
    form_class = MarketingPreferenceForm
    template_name = 'base/forms.html'
    success_url = '/settings/email/'
    success_message = "Your email preferences has been updated"

    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect('/login/?next=/settings/email/')
        return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Email Preferences'
        return context

    def get_object(self):
        user = self.request.user
        if not user.is_authenticated:
            return HttpResponse("Not allowed", status=400)
        obj, created = MarketingPreference.objects.get_or_create(user=user)
        return obj


'''
POST METHOD
data[email]:chadolskii123@gmail.com
data[email_type]:html
data[id]:216c161324
data[ip_opt]:122.43.80.86
data[list_id]:c35d4fd9fa
data[merges][ADDRESS]:data[merges][BIRTHDAY]:
data[merges][EMAIL]:chadolskii123@gmail.com
data[merges][FNAME]:Young Wook
data[merges][LNAME]:Cha
data[merges][PHONE]:data[reason]:manual
data[web_id]:1341559344
fired_at:2020-11-13 07:39:23
type:unsubscribe'''


class MailchimpWebhookView(CsrfExemptMixin, View):  # HTTP GET -- def get() CSRF???
    def post(self, request, *args, **kwargs):
        data = request.POST
        list_id = data.get('data[list_id]')
        if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
            hook_type = data.get('type')
            email = data.get('data[email]')
            response = sub_status = Mailchimp.check_subscription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == 'subscribed':
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == 'unsubscribed':
                is_subbed, mailchimp_subbed = (False, False)
            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPreference.objects.filter(user__email__iexact=email)
                if qs.exists:
                    qs.update(subscribed=False, mailchimp_subscribed=False, mailchimp_msg=str(data))
        return HttpResponse("Thank you", status=200)

# def mailchimp_webhook_view(request):
#     data = request.POST
#     list_id = data.get('data[list_id]')
#     if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
#         hook_type = data.get('type')
#         email = data.get('data[email]')
#         response = sub_status = Mailchimp.check_subscription_status(email)
#         sub_status = response['status']
#         is_subbed = None
#         mailchimp_subbed = None
#         if sub_status == 'subscribed':
#             is_subbed, mailchimp_subbed = (True, True)
#         elif sub_status == 'unsubscribed':
#             is_subbed, mailchimp_subbed = (False, False)
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPreference.objects.filter(user__email__iexact=email)
#             if qs.exists:
#                 qs.update(subscribed=False, mailchimp_subscribed=False, mailchimp_msg=str(data))
#     return HttpResponse("Thank you", status=200)
