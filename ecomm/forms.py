from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "이름 / ID"
        }), label="이름")
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class': 'form-control',
            'placeholder': '연락받을 이메일 주소'
        }
    ),label='메일주소')
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': '메세지'
        }), label='메세지')

    # 예외 처리 !!!
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be gmail.com")
    #     return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong.")
