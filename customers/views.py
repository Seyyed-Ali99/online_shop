from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest,HttpResponseForbidden
from accounts.models import User
from product.models import Product
from .forms import UserRegisterForm , LoginForm
from django.contrib.auth.views import LogoutView , LoginView
from django.views import View
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.


class CustomeLoginView(View):
    template_name = 'login.html'  

    def get(self, request):  
        form = LoginForm()  
        return render(request, self.template_name, {'form': form})  

    def post(self, request):  
        form = LoginForm(request.POST)  
        email = request.POST.get('email')  
        password = request.POST.get('password')  
        user = authenticate(request, email=email, password=password)  

        if user is not None:  
            login(request, user)
            if user.role == "customer":  
                return redirect('customer_dashboard') 
            elif user.role == "admin":
                return redirect('vendor_dashboard')
            else :
                return HttpResponseBadRequest()
        else:  
            messages.error(request, 'Invalid email or password.')  
        return render(request, self.template_name, {'form': form})
    
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

            return redirect('login')
        else :
            return HttpResponseBadRequest()

        

class DashboardUserView(View,LoginRequiredMixin):
   
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=args)
        if user.role == "customer":
            context = {"user":user}
            return render(request, "customer_dashboard.html", context=context)
        elif user.role == "admin" or user.role=="manager" or user.role=="operator":
            context = {"user":user}
            return render(request, "vendor_dashboard.html", context=context)

        else :
            return HttpResponseForbidden()


class UpdateUserView(UpdateView,LoginRequiredMixin):  
    model = User 
    form_class = UserRegisterForm  
    template_name = 'update_user.html'  
    success_url = reverse_lazy('dashboard')  # Redirect to dashboard after update  

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
    
class CustomLogoutView(LogoutView,LoginRequiredMixin):
    """Class-based Logout View with confirmation template."""  
    template_name = 'logout_confirm.html'  # Specify the same template for confirmation  
    next_page = 'home'    

    def post(self, request, *args, **kwargs):  
        """Handle POST request for logout."""  
        self.dispatch(request, *args, **kwargs)  
        return super().post(request, *args, **kwargs)    

        




