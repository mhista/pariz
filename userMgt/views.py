from .models import Address,UserProfile,BankInfo
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
import json
from django.http import JsonResponse
import re
from django.contrib import messages
from django.shortcuts import redirect,reverse
from django.core.exceptions import ObjectDoesNotExist
class createAddress(LoginRequiredMixin,generic.View): 
    re_alpha = '[a-zA-z]'
    re_symbol = ['~','!','@','#','$','%','^','&','*']    
    re_num="[0-9]"
    def post(self,request,*args,**kwargs):
        is_ajax = request.headers.get('X-Requested-With')=='XMLHttpRequest'
        if is_ajax:
            self.data = json.loads(request.POST.get('data'))
            self.validate_form(self.data)
            print(self.data)

    def validate_form(self,data):
        # validates the form, and checking for errors
        if data is None:
            return JsonResponse({'data':'none'})
        else:     
            if len(data) == 3:
                zip = data[0]['zip']
                zip2 = data[1]["szip"]
                ship_phone = data[1]["sphone"]  
                bill_phone = data[0]['phone']  
                cc_cvv = data[2]["cc_cvv"]
                cc_expiry = data[2]["cc_expiry"]
                check2 = [bill_phone,zip,zip2,ship_phone,cc_cvv,cc_expiry]
                o = re.search(self.re_alpha,(self.y for self.y in check2))  
                if o:
                    return JsonResponse({'data':f"only numbers allowed in {self.y}"})
                elif len(ship_phone) >15:
                    return JsonResponse({'data','invalid phone number for ship address please correct'})
                elif len(bill_phone)  > 15:
                    return JsonResponse({'data','invalid phone number for billing address please correct'})
                else:
                    return self.save_billing_info(data)
            else:  
                zip = data[0]["zip"]
                cc_cvv = data[1]["cc_cvv"]
                cc_expiry = data[1]["cc_expiry"]
                bill_phone = data[0]['phone']   
                num_check = [zip,cc_cvv,cc_expiry,bill_phone]
                p = re.search(self.re_alpha,(self.x for self.x in num_check))
                if p:
                    return JsonResponse({'data':f"only numbers allowed in {self.x}"})
                elif len(bill_phone)  > 15:
                    return JsonResponse({'data','invalid phone number for billing address please correct'})
                else:
                    return self.save_billing_info(data)
        
    def save_billing_info(self,list_data):
        '''
        posible test:
        1. user uses default billing address but new shipping address
        2. user uses default shipping address but new billing address
        
        '''
        data = list_data[0]
        print(data)
        fname = data["fname"]
        lname = data["lname"]
        email = data["email"]
        address = data["address"]
        address2 = data["address2"]
        country = data["country_select"]
        phone = data["phone"]
        zip = data["zip"]
        state = data["state_select"]
        self.same_ship = data["same_ship"]
        try:
            # Address.objects.get(user=self.request.user,default=True,address_choice="B")
            addresser = Address.objects.get(user=self.request.user,default=True,address_choice="B")
            """ checks the billing2 address for an address with default set to true, overrides and and sets the new billing2 address as default"""
            addresser.default = False
            addresser.save()
            bill_address = Address(
                user = self.request.user,firstname=fname,lastname=lname,country=country,state=state,address=address,address2=address2,zip=zip,phone=phone,default = True,address_choice= 'B',email=email
            )
            bill_address.save()
            # return data1 = bill
            return self.save_shipping_info(list_data)               
        except Address.DoesNotExist:
            """ this part of the code runs when there is no default billing2 address """
            bill_address2 = Address(
                user = self.request.user,firstname=fname,lastname=lname,country=country,state=state,address=address,address2=address2,zip=zip,phone=phone,default = True,address_choice= 'B',email=email
            )
            bill_address2.save()
            
            return self.save_shipping_info(list_data)
                    
    def save_shipping_info(self,ship_data):
            # checks if the shipping address is to be the same as billing address
            if self.same_ship:
                    # checks the shipping address for an address with default set to true, overrides and and sets the new shipping address as default
                bill = Address.objects.get(user=self.request.user,default=True,address_choice='B')
                try:
                    addressed = Address.objects.get(user=self.request.user,default=True,address_choice="S")
                    addressed.default = False
                    addressed.save()
                    shipping_address = Address(user = self.request.user,firstname=bill.firstname,lastname=bill.lastname,country=bill.country,state=bill.state,address=bill.address, address2=bill.address2,zip=bill.zip,phone=bill.phone,default = True,address_choice= 'S',email=bill.email, same_ship = True
                    )
                    shipping_address.save()
                    return JsonResponse({'data':'address successfully added'})
                except Address.DoesNotExist:
                    shipping_addres = Address(user = self.request.user,firstname=bill.firstname,lastname=bill.lastname,country=bill.country,state=bill.state,address=bill.address, address2=bill.address2,zip=bill.zip,phone=bill.phone,default = True,address_choice= 'S',email=bill.email, same_ship = True
                    )
                    shipping_addres.save()
                    return JsonResponse({'data':'address successfully added'})
            else:
                data = ship_data[1]
                fname = data["sfname"]
                lname = data["slname"]
                email = data["semail"]
                phone = data["sphone"]
                address = data["saddress"]
                address2 = data["saddress2"]
                country = data["scountry_select"]
                zip = data["szip"]
                state = data["sstate_select"]
                    # checks the shipping address for an address with default set to true, overrides and and sets the new shipping address as default
                try:
                    addressed = Address.objects.get(user=self.request.user,default=True,address_choice="S")
                    addressed.default = False
                    addressed.save()
                    shipping_address2 = Address(
                    user = self.request.user,firstname=fname,lastname=lname,country=country,state=state,address=address,address2=address2,zip=zip,phone=phone,default = True,address_choice= 'S',email=email
                    )
                    shipping_address2.save()
                    return JsonResponse({'data':'address successfully added'})
                except Address.DoesNotExist:
                    shipping_address3 = Address(
                    user = self.request.user,firstname=fname,lastname=lname,country=country,state=state,address=address,address2=address2,zip=zip,phone=phone,default = True,address_choice= 'S',email=email
                    )
                    shipping_address3.save()
                    return JsonResponse({'data':'address successfully added'})
                
        # elif len(cc_cvv) > 3:
        #     return JsonResponse({'cvv_error','invalid cvv number please correct'})
        # elif '/' in cc_expiry:
        #     expiry = cc_expiry.strip().split('/')
        #     exp_mnth, exp_yr = expiry[0], expiry[1]
        #     print(exp_mnth,exp_yr)      