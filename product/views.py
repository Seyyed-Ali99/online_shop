from django.shortcuts import render , redirect
from unicodedata import category

from .forms import CategoryForm , ProductForm , CommentForm
from .models import Category , Product , Comment
from django.http import HttpResponse , HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import UpdateView, CreateView , ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class AddProduct(LoginRequiredMixin,View):
    
    def get(self,request):
        form = ProductForm()
        return render(request,"add_product.html",{"form":form})

    def post(self,request):
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_products')
        else :
            return HttpResponseBadRequest()

class ProductList(View):
    
    def get(self,request):
        category_id = request.query_params.get('category')

        products = Product.objects.filter(category_id=int(category_id)).order_by('-id')
        # categories = Category.objects.all()
        context = {"products":products,"categories":category_id}
        return render(request,'shop.html',context)

class ProductDetail(View):
    def get(self,request,*args,**kwargs):
        product = Product.objects.get(id=args)
        context = {'product':product}
        return render(request,'',context=context)

class ProductDelete(LoginRequiredMixin,View):
    def get(self,request):
        pass

    def post(self,request):
        pass


class ProductUpdate(LoginRequiredMixin,UpdateView):
    model = Product 
    form_class = ProductForm  
    template_name = 'update_product.html'  
    success_url = reverse_lazy('product_detail')  # Redirect to dashboard after update  

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
    

class AddCategory(LoginRequiredMixin,View):
    
    def get(self,request):
        form = CategoryForm()
        return render(request,"",{"form":form})

    def post(self,request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else :
            return HttpResponseBadRequest()


class CategoryDelete(LoginRequiredMixin,View):
    def get(self,request):
        pass

    def post(self,request):
        pass


class CategoryUpdate(LoginRequiredMixin,UpdateView):
    model = Category 
    form_class = CategoryForm  
    template_name = 'update_category.html'  
    success_url = reverse_lazy('all_products')  # Redirect to dashboard after update  

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
    

class AddComment(LoginRequiredMixin,View):
    
    def get(self,request):
        form = CommentForm()
        return render(request,"",{"form":form})

    def post(self,request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else :
            return HttpResponseBadRequest()
        
class CommentList(View):
    def get(self,request):
   
        products = Product.objects.all().order_by('-id')
        context = {"products":products}
        return render

class CommentDetail(View):
    pass

class CommentDelete(LoginRequiredMixin,View):
    def get(self,request):
        pass

    def post(self,request):
        pass


class CommentUpdate(LoginRequiredMixin,UpdateView):
    model = Comment 
    form_class = CommentForm  
    template_name = 'update_comment.html'  
    success_url = reverse_lazy('product_detail')  # Redirect to dashboard after update  

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
