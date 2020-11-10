from django.contrib.auth import authenticate, login, get_user_model

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from .forms import ContactForm


def home_page(request):
    context = {
        "title": "Hello World!",
        "content": "welcome to the homepage",
    }
    # print(request.session.get('first_name', 'Unkown')) => getter
    # cart_views에서 first_name이란 이름의 variable을 session에 저장함
    if request.user.is_authenticated:
        context["premium_content"] = "YEAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHH~~~~~~~~"
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title": "About Page!",
        "content": "welcome to the about page"
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    context = {
        "title": "Contact Page!",
        "content": "welcome to the contact page",
        "form": contact_form,
    }

    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission"})

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
