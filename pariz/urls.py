from django.contrib import admin
from django.urls import path, include
# from django.contrib.auth.views import (
#     LoginView,
#     LogoutView,
#     PasswordChangeView,
#     PasswordChangeDoneView,
#     PasswordResetCompleteView,
#     PasswordResetConfirmView,
#     PasswordResetDoneView,
#     PasswordResetView
    
# )



from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path ('', include('parizian.urls',namespace='parizian')),
    path ('apipoint/', include('apipoint.urls',namespace='apipoint')),
    path ('profile/', include('userMgt.urls',namespace='profile')),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

    urlpatterns+=static(settings.STATIC_URL, document_root =settings.STATIC_ROOT)
    # urlpatterns +=static()