from .views import InitiatePayment,VerifyPayment,VerifyAccount,createc,save_items
from django.urls import path
app_name = 'apipoint'

urlpatterns = [
    path('',InitiatePayment.as_view(), name="initiate-payment"),
    path('createc/', createc, name="verify-payment"),
    path('<int:pk>/verify_account/', VerifyAccount.as_view(), name="verify-account"),
    path('save/',save_items,name='save-item'),
    
    
]