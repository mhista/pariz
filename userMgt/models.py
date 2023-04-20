# from xxlimited import Null
import email
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from parizian.models import Category,Item
from stores.models import Stores
from .refs import generate_ref_code

User = get_user_model()
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
    has_bank_details = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True,related_name='ref_by')
    code = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now=True)
    
    def save(self,*args,**kwargs):
        if self.code == '':
            code = generate_ref_code()
            self.code = code
        super().save(*args,**kwargs)

class UserProfile(models.Model):
    profile=models.OneToOneField(Profile,on_delete=models.CASCADE,related_name='profile')
    country = models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    zip_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=30)
    image = models.ImageField(upload_to='',null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
 


class BankInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    account_number = models.CharField(max_length=50)
    card_number = models.IntegerField
    cvv = models.SmallIntegerField
    month = models.SmallIntegerField
    year = models.SmallIntegerField

class Address(models.Model):
    Billing = 'B'
    Shipping = 'S'
    Address_type = [(Billing,'Billing'),(Shipping, 'Shipping')]
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    firstname = models.CharField(max_length=30)
    email= models.EmailField()
    lastname = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    address = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250,null=True,blank=True)
    zip = models.CharField(max_length=10)
    phone =  models.CharField(max_length=30)
    same_ship = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    address_choice = models.CharField(max_length=1,choices=Address_type)
    
    def __str__(self):
        return f"{self.user.username } {self.address_choice}"