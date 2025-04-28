from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest
from django.views import View
from django.views.generic import TemplateView
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