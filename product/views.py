from django.shortcuts import render , redirect
from .forms import CategoryForm , ProductForm , CommentForm
from .models import Category , Product , Comment
from django.http import HttpResponse , HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class AddProduct(View,LoginRequiredMixin):
    
    def get(self,request):
        product

    def post(self,request):
        pass

class ProductList(View):
    pass

class ProductDetail(View):
    pass

class ProductDelete(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass


class ProductUpdate(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass

class AddCategory(View,LoginRequiredMixin):
    
    def get(self,request):
        pass

    def post(self,request):
        pass


class CategoryDelete(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass


class CategoryUpdate(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass
    

class AddComment(View,LoginRequiredMixin):
    
    def get(self,request):
        pass

    def post(self,request):
        pass

class CommentList(View):
    pass

class CommentDetail(View):
    pass

class CommentDelete(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass


class CommentUpdate(View,LoginRequiredMixin):
    def get(self,request):
        pass

    def post(self,request):
        pass
