from django.db import models
from django.shortcuts import reverse
from django.conf import settings
from .file_upload import item_uploads
from stores.models import Stores   
import uuid
user=settings.AUTH_USER_MODEL
class Category(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Item(models.Model):  
    name = models.CharField(max_length=100)
    store = models.ForeignKey(Stores, on_delete=models.CASCADE,null=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True,null=True,default=0)
    # categories = models.CharField(max_length=10,choices=category_choices,default=none)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='category',blank=True,null=True)
    # slug = models.SlugField()
    description = models.TextField(editable=True)
    quantity = models.IntegerField(default=1)
    item_img = models.ImageField(upload_to=item_uploads,null=True)
    has_coupon = models.BooleanField(default=False) 
    create_coupon = models.BooleanField(default=False) 
    
    def __str__(self):
        return self.get_item_name()
    # def add_to_cart_url(self):
    #     return reverse('pickafrica:add-to-cart', kwargs={'pk':self.pk})
    def remove_from_cart_url(self):
        return reverse('pickafrica:add-to-cart', kwargs={'pk':self.pk})
    def get_category(self):
        return self.category.category.name
    def return_store(self):
        return self.store.name
    def get_img(self):
        return self.item_img.url
    def get_item_name(self):
        return self.name[0:20]
    def get_coupon(self):
        return self.item.code
    def save(self,*args,**kwargs):
        if self.create_coupon == True:
            self.has_coupon = True
        super().save(*args,**kwargs)

class OrderItem(models.Model):
    """
    1.when an item is added to the cart, an order_item is created using a foreign key back to the item
    2.when the user adds this same item again, instead of creating a new ordderitem, it is incremented using the quantity field.
    3.the user model provides a way of controlling the transactions here
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey('Order',on_delete=models.CASCADE,related_name='order_item',null=True,blank=True)
    
    def __str__(self):
        return f"{self.quantity} {self.item.name}'s: ordererd by {self.user.username} {self.pk}"
    def get_item_img(self):
        return self.item.item_img.url
    def get_item_price(self):
        return self.item.price
    def get_item_discount(self):
        return self.item.discount_price
    def get_quantity(self):
        return self.quantity
    def get_total_price(self):
        return self.item.price * self.quantity
    
class Order(models.Model):
    """
    1. after the order_item is created, it is pushed into the order table, using a foreign key refernce.
        it allows for many order_items to be linked to the order and chained by the user models.
        this means that the user model controls it.
    """
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True,null=True)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=0)
    from userMgt.models import Address
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="shipping_address", null=True,blank=True)                     
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, related_name="billing_address", null=True,blank=True)
    
    
    def __str__(self):
        return self.user.username
    def get_total_price(self):
        total = 0
        for item in self.order_item.all():
            total += item.get_total_price()
        return total
class Coupon(models.Model):
    code = models.CharField(max_length=20,null=True,blank=True)
    item = models.OneToOneField(Item,on_delete=models.CASCADE,null=True,blank=True,related_name='item')
    expiry_date = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return self.code
    def save(self,*args,**kwargs):
        while not self.code:
            code = str(uuid.uuid4()).replace('-','')[:12]
            object_with_similar_code = Coupon.objects.filter(code=code)
            if not object_with_similar_code:
                self.code = code
        super().save(*args,**kwargs)
        