from random import randrange
from django.shortcuts import render,reverse,get_object_or_404,redirect
from django.utils import timezone
from django.contrib import messages
from django.views import generic,View
from django.contrib.auth.mixins import LoginRequiredMixin
from parizian.mixins import SuperUserRequired
from parizian.models import Category, Item, OrderItem, Order
from django.http import JsonResponse,HttpResponseBadRequest
from stores.models import Stores
class IndexView(generic.View):
  
    def get(self,request,*args,**kwargs):
        # queryset = OrderItem.objects.filter(user=request.user,order__ordered=False).reverse()[:3]
        # context = {'orderItem':queryset}
        return render(request,'index.html')
    
class JsonItemList(LoginRequiredMixin,View):
    # this view uses an ajax call to update the list of items in the home page on a button click
    def get(self,request,*args,**kwargs):
        num_posts = self.kwargs['num_posts']
        visible = 4
        upper = num_posts
        lower = upper - visible
        size =  Item.objects.all().count()
        qs = Item.objects.all()
        try:
            total = Order.objects.get(user=request.user,ordered=False).get_total_price()
        except Order.DoesNotExist:
            total = '0'
        data = []
        for q in qs:
            print(q.get_img())
            item={
                'id':q.pk,
                'name':q.get_item_name(),
                'price':q.price,
                'discount':q.discount_price,
                # 'url': q.add_to_cart_url(),
                'img':q.get_img()
            }
            data.append(item)

        return JsonResponse({'data':{'data':data[lower:upper],'total':total},'size':size})

    
class landing(generic.TemplateView):
    template_name = 'product-checkout.html'
    pass
def save_items(request):
    # import requests
    # import json
    # import random

    # base_url = 'https://fakestoreapi.com/'
    # # base_url = 'https://api.storerestapi.com/'
    
    # path = 'products'
    # path2 = 'products/categories'
    # url = base_url+path
    # url2 = base_url+path2
    # limit=''
    # params = {
    #     'limit':limit
    # }
    # response =requests.get(url)
    # response2 = requests.get(url=url2)
    # res = response.json()
    # res2 = response2.json()
    # # print(res)
    # print(res2)
    # cat = Category.objects.all()
    # for x in res:
    #     print(x)
    #     item = Item(
    #         name=x['title'],
    #         description = x['description'],
    #         store = Stores.objects.first(),
    #         category = cat[random.randrange(len(cat))],
    #         price =  random.randint(600,2000),
    #         discount_price = random.randint(300,500),
    #         quantity=random.randint(5,15)
    #     )
    #     item.save()
        
    # return redirect(request,'index.html')
    pass
   
class ItemDetail(LoginRequiredMixin,generic.DetailView):
    # get the item detail
    template_name = 'product-detail.html'
    queryset = Item.objects.all()
    context_object_name = 'item'
    
class ItemJsonDetail(LoginRequiredMixin,generic.View):
    
    def get(self,request,*args,**kwargs):
        pk= kwargs.get('pk')
        query = Item.objects.get(pk=pk)
        context = {'query':query}
        return render(request,'index.html',context)
    
class AddToCart(LoginRequiredMixin,generic.View):
    # Add Item to cart, and update it if item already exists
    def post(self,request,*args,**kwargs):
        is_ajax =  request.headers.get('X-Requested-With')=='XMLHttpRequest'
        if is_ajax:
            pk = request.POST.get('pk')
            quantity = int(request.POST.get('quantity'))
            item = get_object_or_404(Item,pk=pk)
            
            if item.quantity <= 0:
                    message = messages.success(request,f'{quantity} item is out of stock')
                    return JsonResponse({'data':f'{item.name} Out Of Stock','bool':False})
            
            order,Created = Order.objects.get_or_create(user=request.user,ordered=False)
            order_item,Created = OrderItem.objects.get_or_create(item=item,user=request.user,order=order)
            order_item.quantity += quantity
            order_item.save()
            order.quantity += quantity
            order.save()
            total = order.get_total_price()
            item.quantity-=quantity
            item.save()
            return JsonResponse({'data':{'info':f'{quantity} item removed from cart','body':total}, 'bool':True})
            
          
        return HttpResponseBadRequest('invalid request')
  

class RemoveFromCart(LoginRequiredMixin,generic.View):
    # remove the item from cart
    def post(self,request,*args,**kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            pk = request.POST.get('pk')
            print(pk)
            item = get_object_or_404(Item,pk=pk)
            order = Order.objects.get(user=request.user,ordered=False)
            orderitem = get_object_or_404(OrderItem,user=request.user,item=item,order=order)
            if orderitem:
                quantity = orderitem.quantity
                orderitem.delete()
                order.quantity -= quantity
                order.save()
                total = order.get_total_price()
                item.quantity+=quantity
                item.save()
                return JsonResponse({'data':{'info':f'{quantity} item removed from cart','body':total}})
                
                        
                
class MinusFromCart(LoginRequiredMixin,generic.View):
    # remove one item from a set of the same item
    def post(self,request,*args,**kwargs):
        is_ajax =  request.headers.get('X-Requested-With')=='XMLHttpRequest'
        if is_ajax:
            pk = request.POST.get('pk')
            print(pk)
            quantity = int(request.POST.get('quantity'))
            item = get_object_or_404(Item,pk=pk)
            order = Order.objects.get(user=request.user,ordered=False)
            orderitem = OrderItem.objects.get(user=request.user,item=item,order=order)
            if orderitem:
                orderitem.quantity-=quantity
                orderitem.save()
                order.quantity -= quantity
                order.save()
                total = order.get_total_price()           
                item.quantity+=1
                item.save()
                return JsonResponse({'data':{'info':f'{quantity} item removed from cart','body':total}, 'bool':True})
class ClearCart(LoginRequiredMixin,generic.View):
    # clears a users cart
    def post(self, request,*args,**kwargs):
        is_ajax = request.headers.get("X-Requested-With")=='XMLHttpRequest'
        if is_ajax:
            order = Order.objects.get(user=request.user,ordered=False)
            order.delete()
            return JsonResponse({'data':'your cart has been cleared'})   
           
def little_post_request(request):
    is_ajax =  request.headers.get('X-Requested-With')=='XMLHttpRequest'
    
    if is_ajax:
        pk = request.POST.get('pk')
        message = messages.success(request,f'item removed from cart {pk}')
        return JsonResponse({'added':'an item has been added'})

class ProductCart(LoginRequiredMixin,generic.TemplateView):
    template_name = 'cart.html'
    context_object_name = 'Item'
  
    
class NavbarCart(LoginRequiredMixin,View):
    # this view uses an ajax call to update the list of items in the home page on a button click
    def get(self,request,*args,**kwargs):
        qs = OrderItem.objects.filter(user=self.request.user)
        data = []
        for q in qs:
            item={
                'id':q.item.pk,
                'name':q.item.get_item_name(),
                'price':q.get_item_price(),
                'total':q.get_total_price(),
                'img':q.get_item_img(),
                'quantity': q.quantity
            }
            data.append(item)
        return JsonResponse({'data':data[-3:]})

class UserCart(LoginRequiredMixin,View):
    # this view uses an ajax call to update the list of items in the home page on a button click
    def get(self,request,*args,**kwargs):
        qs = OrderItem.objects.filter(user=self.request.user).reverse()
        data = []
        total = Order.objects.get(user=request.user,ordered=False).get_total_price()
        for q in qs:
            item={
                'id':q.item.pk,
                'name':q.item.get_item_name(),
                'price':q.get_item_price(),
                'total':q.get_total_price(),
                'img':q.get_item_img(),
                'quantity': q.quantity
            }
            data.append(item)
        return JsonResponse({'data':{'data':data,'total':total}})

class SearchQuery(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        search_item = kwargs.get('data')
        print(search_item)
        query = Item.objects.filter(name__icontains=search_item)
        data = []
        for q in query:
            item={
                'id':q.pk,
                'name':q.name,
                'price':q.price,
                'discount':q.discount_price,
                'slug':q.slug,
                # 'url': q.add_to_cart_url(),
                'img':q.get_img()
                }
            data.append(item)
        return JsonResponse({'query':data})
class Checkoutview(LoginRequiredMixin,generic.ListView):
    template_name = 'checkout.html'
    context_object_name = 'Item'
    
    def get_queryset(self):
        queryset = OrderItem.objects.filter(user=self.request.user, order__ordered=False)
        return queryset
    def get_context_data(self, **kwargs):
        context = super(Checkoutview,self).get_context_data(**kwargs)
        order = Order.objects.get(user=self.request.user,ordered=False)
        context['quantity'] = order.quantity
        from userMgt.models import Address
        from apipoint.utils import PayStack
        bank_name = ''
        query = [1,2,3,4,5]
        # bank_data,value = PayStack.get_bankcode(bank_name)
        # for x in bank_data:
        #     x = bank_data['name']
        #     query.append(x)
        context['bank_name'] = query
        ship = Address.objects.filter(user=self.request.user, default=True,address_choice='S')
        bill = Address.objects.filter(user=self.request.user, default=True,address_choice='B')
        if ship.exists():
            context['ship'] = ship
        if bill.exists():
            context['bill'] = bill
        return context
    
class CheckoutProcess(LoginRequiredMixin,View):
    def post(self,request,*args,**kwargs):
        is_ajax =  request.headers.get('X-Requested-With')=='XMLHttpRequest'
        if is_ajax:
            type = request.POST.get("type")
            log = request.POST.get("bool")
            print(log)
            from userMgt.models import Address
            order = Order.objects.get(user=self.request.user,ordered=False)
            ship = Address.objects.get(user=request.user,address_choice=type,default=True)
            if type == 'S' and log == 'true':
                order.shipping_address = ship
                order.save()       
                return JsonResponse({'data':f'default {type}  address used'})    
            elif type == 'B' and log == 'true':
                order.billing_address = ship
                order.save()       
                return JsonResponse({'data':f' default {type}  address used'})
            elif log == 'false':
                if type == 'B':
                    order.billing_address = None
                    order.save()                    
                    return JsonResponse({'data':f' {type} address has been removed'})
                elif type == 'S':
                    order.shipping_address = None
                    order.save()       
                    return JsonResponse({'data':f' {type} address has been removed'})
            else:
                return JsonResponse({'data':f'no default address saved'})
            
            