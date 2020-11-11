import stripe
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url

from billing.models import BillingProfile, Card

STRIPE_PUB_KEY = 'pk_test_51HmCc1Lp7u52kdKrJKoYnLkrB7Tb8oXLLs2mSRrOqqKN4o7ASWXWp54iDc4osi1Z1xDooarv1z6VlVz1ctSoEe9T00KAIxZLed'
#STRIPE_PUB_KEY = 'sk_test_51HmCc1Lp7u52kdKryw1nKeAjvR51vJww9gHTbNm6OZuk4pq26dKQT1Qv2tbdcaMaHF7oSf0kdb8ovkEjaK5ael4X00TiJhLpJW'

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
            new_card_obj = Card.objects.add_new(billing_profile=billing_profile, stripe_card_response=token)

        return JsonResponse({"message": "Success your Card is added"})
    return HttpResponse("error", status_code=401)
