from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Stores
user = get_user_model()

class CreateStoreForm(forms.ModelForm):
    class Meta:
        model = Stores
        fields =('name','reg_no',)
        


