from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.http import is_safe_url

from accounts.forms import LoginForm, RegisterForm, GuestForm
from accounts.models import GuestEmail


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            redirect("/register/")
    return redirect("/register/")


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guset_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                redirect("/")

            # context['form'] = LoginForm()
            return redirect("/")
        else:
            print("Error")
    return render(request, "accounts/login.html", context)


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
        return redirect("login")
    else:
        return render(request, "accounts/register.html", context)
