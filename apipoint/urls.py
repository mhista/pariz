from .views import InitiatePayment,VerifyPayment,VerifyAccount,createc
from django.urls import path
app_name = 'apipoint'

urlpatterns = [
    path('',InitiatePayment.as_view(), name="initiate-payment"),
    path('createc/', createc, name="verify-payment"),
    path('<int:pk>/verify_account/', VerifyAccount.as_view(), name="verify-account"),
    
    
]