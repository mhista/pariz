from django.shortcuts import render
from .models import Stores
from django.shortcuts import render,reverse
from .forms import CreateStoreForm
from django.views import generic
from django.core.mail import send_mail
# from pickafrica.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

class CreateStore(LoginRequiredMixin,generic.CreateView):
    """
    Deals with creating stores
    """
    model = Stores
    form_class = CreateStoreForm
    template_name = 'create-store.html'
    
    def form_valid(self, form):
        user = self.request.user
        new_form = form.save(commit=False)
        new_form.user = user
        new_form.save()
        user.has_store = True
        user.save()
        return super(CreateStore,self).form_valid(form)
    def get_success_url(self):
        return reverse('pickafrica:index')
