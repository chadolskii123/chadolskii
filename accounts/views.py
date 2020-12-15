from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

# Create your views here.
from django.template.context_processors import request
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, FormView, DetailView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin, UpdateView

from accounts.forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm
from accounts.models import GuestEmail, EmailActivation
from accounts.signals import user_logged_in

# 함수형 선언
# @login_required
# def account_home_view(request):
#     return render(request, "accounts/home.html", {})

#  클래스형 선언
from ecomm.mixins import NextUrlMixin, RequestFormAttachMixin


class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = "accounts/home.html"

    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin, View):
    success_url = '/login'
    form_class = ReactivateEmailForm

    def get(self, request, key=None, *args, **kwargs):
        self.key = key
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.confirmable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(request, "인증이 완료되었습니다. 로그인 해주세요 :)")
                return redirect("login")
            else:
                activate_qs = qs.filter(activated=True)
                if activate_qs.exists():
                    reset_link = reverse("password_reset")
                    msg = f"""이미 인증된 아이디 입니다. 혹시 비밀번호를 잊으셨나요? <a href="{reset_link}">비밀번호 재설정 하기</a>
                    """
                    messages.success(request, mark_safe(msg))
                    return redirect("login")

        context = {"form": self.get_form(), 'key': key}
        return render(request, 'registration/activation-error.html', context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = f"""승인 메일 재전송 완료
        """
        messages.success(self.request, mark_safe(msg))
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()

        return super(AccountEmailActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {"form": form, "key": self.key}
        return render(self.request, 'registration/activation-error.html', context)


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
            redirect("/login/")
    return redirect("/register/")


# Mixin 안에 함수들을 넣어서 Form의 값을 self에 담아 줄 수 있다.!!!!!!!!!
class LoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = "accounts/login.html"
    default_next = "/"

    def form_valid(self, form):
        next_url = self.get_next_url()
        return redirect(next_url)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/login/'

    def form_valid(self, form):
        messages.success(self.request, "인증메일이 전송되었습니다.")
        return super().form_valid(form)


class UserDetailChangeView(LoginRequiredMixin, UpdateView):
    form_class = UserDetailChangeForm
    template_name = 'accounts/detail_update_view.html'

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super(UserDetailChangeView, self).get_context_data(**kwargs)
        context['title'] = 'Change Your Account Details'
        return context

    def get_success_url(self):
        return reverse("accounts:home")