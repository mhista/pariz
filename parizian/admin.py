from django.contrib import admin
from .models import Item, OrderItem, Order,Category,Coupon
# Register your models here.

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Coupon)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name','price','has_coupon','get_coupon')
admin.site.register(Item,ItemAdmin)
