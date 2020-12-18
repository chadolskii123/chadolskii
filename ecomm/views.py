from django.contrib.auth import authenticate, login, get_user_model
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from products.models import Product
from django.core.mail import send_mail
from .forms import ContactForm


def home_page(request):
    object_list = Product.objects.all()
    context = {
        "object_list" : object_list
    }
    if request.user.is_active :
        if request.user.is_admin :
            return redirect("sales_analytics")
    else :
        return render(request, 'home_page.html', context)


def juso_page(request):
    return render(request, 'addresses/juso.html')

def introduce_page(request):
    return render(request, 'introduce.html')

def about_page(request):
    context = {
        "title": "About Page!",
        "content": "welcome to the about page"
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "건의 사항",
        "content": "",
        "form": contact_form,
    }

    if contact_form.is_valid():
        if request.is_ajax():
            subject = request.POST.get('fullname')+" / " + request.POST.get("email")
            message = request.POST.get('content')
            sent_mail = send_mail(subject=subject, message =message, from_email = settings.EMAIL_HOST_USER, recipient_list=settings.EMAIL_HOST_USER, fail_silently=True)
            
            if sent_mail :
                msg = {"message" : "확인 후 연락 드리겠습니다."}
            else :
                msg = {"message" : "죄송합니다. 전송 실패하였습니다."}

            return JsonResponse(msg)

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    #
    # if request.method == "POST":
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)
