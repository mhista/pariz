from django.contrib import admin
# Register your models here.
from .models import UserProfile, BankInfo, Address
admin.site.register(UserProfile)
admin.site.register(BankInfo)
admin.site.register(Address)
