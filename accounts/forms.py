from django import forms
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, user_logged_in
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

from accounts.models import EmailActivation

User = get_user_model()


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField(label="이메일")


    def clean_data(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.eamil_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = f"""This email does not exists, would you like to register? 
would you like to <a href="{register_link}"> register</a>?"""

            raise forms.ValidationError(mark_safe(msg))
        return email


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name', 'email', 'password', 'is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class GuestForm(forms.Form):
    email = forms.EmailField()


class LoginForm(forms.Form):
    email = forms.EmailField(label='이메일')
    password = forms.CharField(label="비밀번호", widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        request = self.request
        data = self.cleaned_data
        email = data.get("email")
        password = data.get("password")
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check active/email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                # not active, check email activation
                link = reverse("accounts:resend_activation")
                reconfirm_msg = """<a href='{resend_link}'>
                승인메일 재전송 하기</a>""".format(resend_link=link)
                confirm_email = EmailActivation.objects.filter(email=email)
                is_confirmable = confirm_email.confirmable().exists()
                if is_confirmable:
                    msg1 = "이메일을 확인하여 승인해주세요.<br>메일을 못찾으시겠다면 오른쪽 링크를 눌러서 재전송 요청해주세요. " +reconfirm_msg.lower()
                    messages.success(request, mark_safe(msg1))
                    raise forms.ValidationError("")
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg2 = "Email not confirmed. " +reconfirm_msg
                    messages.success(request, mark_safe(msg2))
                    raise forms.ValidationError(mark_safe(msg2))
                if not is_confirmable and email_confirm_exists:
                    messages.success(request, "해당 사용자는 비활성 상태입니다.")
                    raise forms.ValidationError("This user is inactive.")

        user = authenticate(request, username=email, password=password)
        if user is None:
            messages.success(request, "가입된 아이디가 없습니다.")
            raise forms.ValidationError("Invalid credentials")
        login(request, user)
        self.user = user
        user_logged_in.send(user.__class__, user=user, request=request)
        try:
            del request.session['guest_email_id']
        except:
            pass
        return data


class RegisterForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='비밀번호', widget=forms.PasswordInput)
    password2 = forms.CharField(label='비밀번호 확인', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name', 'email',)

        labels = {
            'full_name': '이름',
            'email': '이메일',
            'password1': '비밀번호',
            'password2': '비밀번호 확인'
        }

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.is_active = False  # send confirmation email
        if commit:
            user.save()
        return user
