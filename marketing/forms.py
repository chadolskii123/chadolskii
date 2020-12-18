from django import forms

from marketing.models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='마케팅 메일을 받으시겠습니까?', required=False)

    class Meta:
        model = MarketingPreference
        fields = ['subscribed']
