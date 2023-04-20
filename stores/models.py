from django.db import models
from django.conf import settings
user=settings.AUTH_USER_MODEL
# Create your models here.
class Stores(models.Model):
    user = models.OneToOneField(user,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=50,verbose_name='business name')
    reg_no = models.CharField(max_length=50,verbose_name='business registration number')
    # category = models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):  
        return self.name
