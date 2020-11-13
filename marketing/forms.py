from django import forms

from marketing.models import MarketingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)

    class Meta:
        model = MarketingPreference
        fields = ['subscribed']
