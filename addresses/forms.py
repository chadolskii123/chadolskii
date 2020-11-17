from django import forms

from addresses.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'country',
            'state',
            'city',
            'address_line_1',
            'address_line_2',
            'postal_code',
        ]
        labels = {
            # 'billing_profile',
            # 'address_type',
            'country': "시",
            'state': "구",
            'city': "동",
            'address_line_1' : "주소 1",
            'address_line_2': "주소 2",
            'postal_code':"우편번호",
        }
