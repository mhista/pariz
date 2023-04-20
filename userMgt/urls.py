from django.urls import path,include
from .views import createAddress
app_name = 'profile'


urlpatterns = [
    path('create-address/', createAddress.as_view(),name='create-address'),
    path('payment/', createAddress.as_view(),name='payment'),
    
]
