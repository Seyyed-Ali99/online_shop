from django.shortcuts import render , redirect
from unicodedata import category
from .forms import CategoryForm , ProductForm , CommentForm,RateForm
from .models import Category , Product , Comment,Rate
from django.http import HttpResponse , HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic import UpdateView, CreateView , ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

class AddProduct(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request):
        form = ProductForm()
        return render(request,"add_product.html",{"form":form})

    def post(self,request):
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
        else :
            return HttpResponseBadRequest()

# class AllComment(LoginRequiredMixin,View):
#     login_url = 'login'
#     def get(self,request):
#         product = Product.objects.get(store=request.user.id)
#         comments = Comment.objects.filter(product=product)
#         return render(request,"stores_comments.html",context={"comments":comments})

class ProductList(View):
    
    def get(self,request):
        category_name = request.GET.get('category',None)
        categories = Category.objects.all()
        print(category_name)

        if category_name :
            products = Product.objects.filter(category__name=category_name)


            # products = Product.objects.filter(category_id=int(category_id)).order_by('-id')
            # categories = Category.objects.all()
        else :
            products = Product.objects.all().order_by('-id')
        context = {"products":products,"categories":categories}
        return render(request,'shop.html',context)
class ProductDetail(View):
    def get(self,request,*args,**kwargs):
        product = Product.objects.get(id=kwargs['id'])
        comments = Comment.objects.filter(related_product=product).order_by('-id')
        rates = Rate.objects.filter(product=product)
        sum = 0
        ratings = 0
        for rate in rates:
            ratings += rate.rate
            sum += 1
        avg = ratings / sum

        context = {'product':product,'rates':avg,'comments':comments}

        return render(request,'product_detail.html',context=context)

class ProductDelete(LoginRequiredMixin,View):
    def get(self,request):
        pass

    def post(self,request):
        pass


class ProductUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'email_login'
    model = Product 
    form_class = ProductForm
    template_name = 'update_product.html'  
    success_url = reverse_lazy('shop_products')


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
    login_url = 'email_login'
    template_name = 'add_comment.html'


    def get(self,request,*args,**kwargs):
        form = CommentForm(initial={'related_product':Product.objects.get(id=kwargs['id']),'user':request.user})
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        form = CommentForm(request.POST,initial={'related_product':Product.objects.get(id=kwargs['id']),'user':request.user})

        if form.is_valid():
            form.save()
            product = Product.objects.get(id=kwargs['id'])
            return redirect('product_detail', product.id)
        else :
            return redirect('shop')



class CommentList(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request):
        comments = Comment.objects.filter(user=request.user.id)
        context = {'comments':comments}
        return render(request,'comments_list.html',context=context)

class CommentDetail(View):
    pass

# class CommentDelete(LoginRequiredMixin,View):
#     def get(self,request):
#         pass
#
#     def post(self,request):
#         pass


class AddRate(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request,*args,**kwargs):
        product = Product.objects.get(id=kwargs['id'])
        rateform = RateForm()
        return render(request,"shop-single.html",context={"rateform":rateform,"product":product})

    def post(self,request):
        rateform = RateForm(request.POST)
        if rateform.is_valid():
            rateform.save()
            return redirect('order_detail')
        else:
            return HttpResponseBadRequest()