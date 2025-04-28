from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest,HttpResponseForbidden
from accounts.models import User
from product.models import Product,Comment
from .forms import UserRegisterForm , EmailLoginForm
from django.contrib.auth.views import LogoutView , LoginView
from django.views import View
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
import random

# Create your views here.


class EmailLoginView(View):
    template_name = 'email_login.html'

    def get(self, request):  
        form = EmailLoginForm()
        return render(request, self.template_name, {'form': form})  

    def post(self, request):  
        form = EmailLoginForm(request.POST)
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        user = authenticate(request, email=email, password=password)  

        if user:
            print("here")
            login(request, user)
            return redirect('dashboard_user')

        else:  
            messages.error(request, 'Invalid email or password.')
            # print("no login")
        return render(request, self.template_name, {'form': form})

class OTPLogin(View):
    template_name = 'otp_login.html'
    def get(self, request,*args,**kwargs):
        pass


class OTPVerify(View):
    template_name = 'otp_verify.html'
    def get(self, request,*args,**kwargs):
        pass
class RegisterView(View):
    template_name = 'register.html'   

    def get(self,request):
        form = UserRegisterForm() 
        return render(request,self.template_name,{'form':form})
    
    def post(self,request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')  

            return redirect('email_login')
        else :
            return HttpResponseBadRequest()

        

class DashboardUserView(LoginRequiredMixin,View):
   
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=kwargs['id'])
        if user.role == "customer":
            comments = Comment.objects.filter(user=user)
            context = {"user":user,"comments":comments}
            return render(request, "customer_panel.html", context=context)
        elif user.role == "admin" or user.role=="manager" or user.role=="operator":
            context = {"user":user}
            return render(request, "vendor_panel.html", context=context)

        else :
            return HttpResponseForbidden()


class UpdateUserView(LoginRequiredMixin,UpdateView):
    model = User 
    form_class = UserRegisterForm  
    template_name = 'update_user.html'  
    success_url = reverse_lazy('dashboard_user')  # Redirect to dashboard after update

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
    
class CustomLogoutView(LoginRequiredMixin,LogoutView):
    """Class-based Logout View with confirmation template."""  
    template_name = 'logout.html'  # Specify the same template for confirmation
    next_page = 'home'    

    def post(self, request, *args, **kwargs):  
        """Handle POST request for logout."""  
        self.dispatch(request, *args, **kwargs)  
        return super().post(request, *args, **kwargs)    

        




