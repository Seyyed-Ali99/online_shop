from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest
from django.views import View
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = "index.html"
    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)