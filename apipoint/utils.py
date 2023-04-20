# from tokenize import blank_re
import requests
from django.conf import settings
class PayStack:
    PAYSTACK_SECRET_KEY = settings.PAYSTACK_SECRET_KEY
    headers={
        'Authorization' :f"Bearer {PAYSTACK_SECRET_KEY}",
        'content-type' :'application/json'
        }
    def __init__(self):
        self.base_url = 'https://api.paystack.co/'
       
    def verify_payment(self,*args,**kwargs):
        path = ''
        url = self.base_url+path
        response = requests.get(url,headers=self.headers)
        if response.status_code == '200':
            response_data = response.json()
            return response_data["status"],response_data["data"]
        response_data=response.json()
        return response_data["status"],response_data["message"]

    def get_bankcode(self,bank_name,*args,**kwargs):
        path = 'bank'
        url = self.base_url+path
        response = requests.get(url)
        if response.status_code == 200:
            print('success')
            response_data = response.json()
            bank_data = response_data["data"]
            print(type(bank_data))
            print(len(bank_data))
            end = len(bank_data)
            start = 0
            bank_name = bank_name
            if bank_name != '':
                while start <= end:
                    mid = (end + start)//2
                    mid_number = bank_data[mid]
                    if bank_name == mid_number['name']:
                        print(mid_number['name'])
                        return mid_number['code']
                    elif mid_number['name'] < bank_name:
                        print(mid_number['name'])
                        start = mid
                    elif mid_number['name'] > bank_name:
                        print(mid_number['name'])
                        end = mid
                    else:
                        return 'invalid detail'
            return 'invalid detail'
        response_data = response.json()
        return response_data['message']
    def validate_account(self,bank_name,account):
        print(bank_name)
        bank_code = self.get_bankcode(bank_name)
        print(bank_code)
        account = account
        path = f'bank/resolve?account_number={account}&bank_code={bank_code}'
        url = self.base_url+path
        response = requests.get(url,headers=self.headers)
        if response.status_code == 200:
            response_data = response.json()
            print(response_data['data'])
            return response_data['message'],bank_code,response_data['data']
        response_data = response.json()
        return response_data['message'],bank_name,response_data["status"]
paystack = PayStack()
