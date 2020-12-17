from django import forms

from addresses.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            #'address_type',
            'postal_code',
            'address_line_1',
            'address_line_2',
            'state',

        ]
