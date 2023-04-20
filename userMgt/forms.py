from .models import Address
from django.forms import ModelForm

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = (
        'firstname',
        'lastname',
        'country',
        'state',
        'address',
        'suite',
        'zip',
        'phone',
        'Company_name',
        'same_ship'
        )