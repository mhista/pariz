from django.urls import path,include

from parizian.views.ItemViews import Checkoutview

from .views import (
    IndexView, 
    ItemDetail,
    Checkoutview,
    CheckoutProcess,
    AddToCart,
    JsonItemList,
    little_post_request,
    ItemJsonDetail,
    ProductCart,NavbarCart,
    MinusFromCart,
    RemoveFromCart,
    UserCart,
    SearchQuery,
    save_items,
    ClearCart
    
    )

app_name = 'parizian'

urlpatterns = [
    path('',IndexView.as_view(), name='index'),
    path('product-detail/<int:pk>/', ItemDetail.as_view(), name='product-detail'),
    path('add-to/', little_post_request, name='little'),
    
    path('checkout/', Checkoutview.as_view(), name='checkout'),
    path('process-checkout/', CheckoutProcess.as_view(), name='process-checkout'),
    path('product-cart/', ProductCart.as_view(), name='product-cart'),
    
    path('search/<str:data>',SearchQuery.as_view(),name='search-item'),
    path('save/',save_items,name='save-item'),
]
jsonPatterns = [
    path('add-to-cart/', AddToCart.as_view(), name='add-to-cart'),
    path('minus-cart/', MinusFromCart.as_view(), name='minus-from-cart'),
    path('remove-cart/', RemoveFromCart.as_view(), name='remove-from-cart'),
    path('hello-world/<int:num_posts>/', JsonItemList.as_view(),name='hello-world'),
    path('nav-cart/', NavbarCart.as_view(), name='nav-cart'),
    path('user-cart/', UserCart.as_view(), name='user-cart'),
    path('clear-cart/', ClearCart.as_view(), name='clear-cart'),
    
    
    
]
urlpatterns += jsonPatterns