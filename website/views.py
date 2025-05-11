from tkinter import Listbox

from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest
from django.views import View
from django.views.generic import TemplateView, ListView
from product.models import Product

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"
    def get(self,request,*args,**kwargs):
        products = Product.objects.all().order_by('-id')[:5]
        context = {"products":products}
        return render(request,self.template_name,context=context)

class Shop(TemplateView):
    template_name = "shop.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)

class ShopSingle(TemplateView):
    template_name = "shop-single.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)

class About(TemplateView):
    template_name = "about.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)

class ContactUs(TemplateView):
    template_name = "contact.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)


class SearchHome(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q','')
        if query:
            return Product.objects.filter(name__icontains=query)
        else:
            return Product.objects.none()

    def get_context_data(self, **kwargs):
        context = super(SearchHome, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q','')
        return context




