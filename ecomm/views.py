from django.contrib.auth import authenticate, login, get_user_model

from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ContactForm, LoginForm, RegisterForm


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
        print(contact_form.cleaned_data)
    #
    # if request.method == "POST":
    #     print(request.POST.get('fullname'))
    #     print(request.POST.get('email'))
    #     print(request.POST.get('content'))
    return render(request, 'contact/view.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    print("User Logged in")
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            # context['form'] = LoginForm()
            return redirect("/")
        else:
            print("Error")
    return render(request, "auth/login.html", context)


def register_page(request):
    user = get_user_model()
    form = RegisterForm(request.POST or None)
    context = {
        "form": form,
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = user.objects.create_user(username, email, password)
        print(new_user)
    return render(request, "auth/register.html", context)
