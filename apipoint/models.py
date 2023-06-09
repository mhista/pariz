from django.db import models
from userMgt.models import BankInfo
from django.conf import settings
import secrets
from .utils import PayStack
# Create your models here.

class PayStackModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True,blank=True)
    bank = models.CharField(max_length=100,null=True,blank=True)
    amount=models.PositiveIntegerField()
    ref=models.CharField(max_length=200)
    cache_id = models.CharField(max_length=100,null=True)
    email=models.EmailField()
    account = models.CharField(max_length=10,null=True,blank=True)
    bank_code = models.CharField(max_length=200,null=True,blank=True)
    card_details = models.CharField(max_length=100,null=True,blank=True)
    verified=models.BooleanField(default=False)
    date_created=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_created',)
    def __str__(self):
        return f"Payment: {self.amount}"
    
    def save(self, *args, **kwargs):
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similer_ref = PayStackModel.objects.filter(ref=ref)
            if not object_with_similer_ref:
                self.ref = ref
        super().save(*args,**kwargs)
    def amount_value(self):
        return self.amount * 100
    def verify_payment(self):
        paystack = PayStack()
        status,result = paystack.verify_payment(self.ref,self.amount)
        if status:
            if result['amount'] /100 == self.amount:
                self.verified = True
                self.save()
        if self.verified:
            return True
        return False
            
                