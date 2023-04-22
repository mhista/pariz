from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.views import generic,View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PayStackModel
from django.conf import settings
from .utils import paystack
import json
from django.http import JsonResponse
import requests
from django.forms.models import model_to_dict
import uuid
# Create your views here.

class InitiatePayment(LoginRequiredMixin,View):
    def post(self,request,*args, **kwargs):
        payment = self.request.body
        payment = json.loads(payment)
        print(payment)
        if payment is not None:
            self.bank_name,self.acct_num=payment['bank_name'],payment['acct_num']
            message,bank_dt,data= paystack.validate_account(self.bank_name,self.acct_num)
            if message:
                payment_info = PayStackModel(email=payment['acct_email'],account=self.acct_num,bank=self.bank_name,bank_code=bank_dt,user=self.request.user,amount=payment['amnt'],cache_id=payment['unique_ref'])
                payment_info.save()
                info = PayStackModel.objects.get(user=self.request.user,cache_id=payment['unique_ref'])
                obj = model_to_dict(info)
                return JsonResponse({'data':data, 'payment':obj, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
            return JsonResponse({'data':'account validation failed'})

    # def validate_form(self, payment):
        
    #         print(message,data)
    #         # pay = PayStackModel(amount=payment['amount'],bank_code=pay)
    #         # self.payment = form.save()
    #         return render(self.request, 'make_payment.html', {'payment':self.payment, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})
   
    
class VerifyPayment(View):
    def get(self,*args,**kwargs):
        payment = get_object_or_404(PayStackModel,ref=kwargs['ref'])
        verified = payment.verify_payment()
        if verified:
            messages.success(self.request,"verification successful")
        else:
            messages.error(self.request, "verification failed")
        return redirect('initiate-payment')
def save_items(request):
    from parizian.models import Category,Item
    from stores.models import Stores
    import requests
    import json
    import random

    base_url = 'https://fakestoreapi.com/'
    # base_url = 'https://api.storerestapi.com/'
    
    path = 'products'
    path2 = 'products/categories'
    url = base_url+path
    url2 = base_url+path2
    limit=''
    params = {
        'limit':limit
    }
    response =requests.get(url)
    response2 = requests.get(url=url2)
    res = response.json()
    res2 = response2.json()
    # print(res)
    print(res2)
    cat = Category.objects.all()
    for x in res:
        print(x)
        item = Item(
            name=x['title'],
            description = x['description'],
            store = Stores.objects.first(),
            category = cat[random.randrange(len(cat))],
            price =  random.randint(600,2000),
            discount_price = random.randint(300,500),
            quantity=random.randint(5,15)
        )
        item.save()
        
    return redirect(request,'index.html')
    
def createc(request):
    from parizian.models import Item,Coupon

    item = Item.objects.all()
    
    for ite in range(1,19,2):
        cap = Coupon()
        cap.save()
        # item[ite].has_coupon = True
        item[ite].save()
        
            

        
        
class VerifyAccount(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        account = get_object_or_404(PayStackModel,user__id=kwargs['pk'])
        print(account)
        verified = account.validate_account()
        if verified:
             messages.success(self.request,"verification successful")
             return redirect('index')
        else:
            messages.error(self.request, "verification failed")
            return redirect('mgt:initiate-payment')