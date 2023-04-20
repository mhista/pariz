from email.mime import application
from urllib.parse import urlencode
import json
import datetime
import requests
from django.http import JsonResponse
from humanfriendly import format_timespan
from django.conf import settings
from django.shortcuts import redirect

def FormError(*args):
    """handles form error that are passed back to the Ajax calls
    """
    message =''
    for f in args:
        if f.errors:
            message = f.errors.as_text()
    return message

def reCAPTCHAValidaation(token):
    """recaptcha validation"""
    url ='https://www.google.com/recaptcha/api/siteverify'
    data = {
        'secret':settings,
        'response':token
    }
    result = requests.post(url,data)
    return result.json()


def redirect_params(**kwargs):
    """
    used to append url parameteres when redirecting users
    """
    url = kwargs.get('url')
    params = kwargs.get('params')
    response = redirect(url)
    if params:
        query_string = urlencode(params)
        response['location'] += '?' + query_string
    return response

class AjaxMixin(object):
    """
    mixin to ajaxify django form -
    """
    def form_invalid(self,form):
        response = super(AjaxMixin,self).form_invalid(form)
        if self.request.is_ajax():
            message = FormError(form)
            return JsonResponse({'result':'error','message':message})
        return response
    def form_valid(self,form):
        response = super(AjaxMixin,self).form_valid(form)
        if self.request.is_ajax:
            form.save()
            return JsonResponse({'result':'Success','message':' '})
        return response
    
def Direction(*args,**kwargs):
    lat_a = kwargs.get('lat_a')
    long_a = kwargs.get('long_a')
    lat_b = kwargs.get('lat_b')
    long_b = kwargs.get('long_b')
    lat_c = kwargs.get('lat_c')
    long_c = kwargs.get('long_c')
    lat_d = kwargs.get('lat_d')
    long_d = kwargs.get('long_d')
    
    origin = f'{lat_a},{long_a}'
    destination = f'{lat_b},{long_b}'
    waypoints= f'{lat_c},{long_c}|{lat_d},{long_b}'
    result = requests.get(
        'https://maps.google.com/maps/api/directions/json?',
        params={
            'origin':origin,
            'destination':destination,
            'waypoints':waypoints,
            'key':''
        }
    )
    directions = result.json()
    if directions["status"]=="ok":
        routes = directions["routes"][0]["legs"]
        print(routes)
        distance = 0
        duration = 0
        route_list = 0
        
        for route in range(len(routes)):
            distance += int(routes[route]["distance"]["value"])
            duration += int(routes[route]["duration"]["value"])
            
            route_step = {
                'origin':routes[route]["start_address"],
                'destination':routes[route]["end_address"],
                'distance':routes[route]["distance"]["text"],
                'duration':routes[route]["duration"]["text"]
                
                
            }         
            

class PaystackModule:
    PAYSTACK_SECRET_KEY=''
    base_url = 'https://api.paystack.co'
    
    def validate_account(self,account,bank_code,*args,**kwargs):
        path = f'/bank/resolve?'
        params = {
            'account_number':account,
            'bank_code':bank_code
        }    
        headers = {
            "Authorization": f"Bearer {self.PAYSTACK_SECRET_KEY}",
            "content_type":"application/json"
        }
        url=self.base_url+path
        response = requests.get(url,params,headers=headers)
        if response.status_code == 200:
            response_data = response.json()
            return response_data["status"],response_data["data"]
        response_data = response.json()
        return response_data["status"],response_data["message"]
    