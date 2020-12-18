import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile, Card


STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY")

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY")
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.
def payment_method_view(request):
    # if request.user.is_authenticated:
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect("/cart/")

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment_method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})


def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status_code=401)
        token = request.POST.get("token")
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_response = stripe.Customer.create_source(customer.id, source=token)
            # new_card_obj = Card.objects.add_new(billing_profile=billing_profile, stripe_card_response=card_response)
            new_card_obj = Card.objects.add_new(billing_profile=billing_profile, token=token)

        return JsonResponse({"message": "카드가 정상적으로 추가되었습니다."})
    return HttpResponse("error", status_code=401)
