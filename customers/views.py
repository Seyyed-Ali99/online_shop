# from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import check_password
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest,HttpResponseForbidden
from accounts.models import User
from product.models import Product,Comment
from .forms import UserRegisterForm, EmailLoginForm, OTPPhoneForm
from django.contrib.auth.views import LogoutView , LoginView
from django.views import View
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView , CreateView , UpdateView,FormView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import OTPPhoneForm,OTPCodeForm
import random
from kavenegar import *

# Create your views here.


class EmailLoginView(View):
    template_name = 'email_login.html'
    # # form_class = EmailLoginForm
    # redirect_authenticated_user = True
    # success_url = reverse_lazy('dashboard_user')

    def get(self, request):
        form = EmailLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EmailLoginForm(request.POST)
        # # print(form)
        # # username = request.POST.get('email')
        # username = "alihoseini"
        # password = request.POST.get('password')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # print(username, password)
            # print(check_password(password,encoded='pbkdf2_sha256$1000000$ED02ywjmAe81f9RK7sxK4d$mCn3tMDGT4fsHJye1pGKfJBWGe39iaxS+FHH2GdTTG8='))
            user = authenticate( username=username, password=password)
            # print(user)

            if user:
                # print(" user exists")
                login(request, user)
                return redirect('dashboard_user')

            else:
                messages.error(request, 'Invalid email or password.')
                # print("no login")
            return render(request, self.template_name, {'form': form})

class OTPLogin(FormView):
    template_name = 'otp_login.html'
    form_class = OTPPhoneForm
    success_url = reverse_lazy('otp_verify')

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        otp = str(random.randint(1000,9999))
        self.request.session['otp'] = otp
        self.request.session['phone'] = phone

        api = KavenegarAPI('31575A4F464F494D76616C6F70634A4968636E76683561502F567746777272784132755279435957514A413D')
        try :
            params = {
                'sender' : '2000660110',
                'receptor': phone,
                'message': f'Your verification code is : {otp}'
            }
            print(params)
            api.sms_send(params)
        except Exception as e:
            form.add_error(None, f"Error sending SMS: {e}")
            return self.form_invalid(form)

        return super().form_valid(form)



class OTPVerify(FormView):
    template_name = 'otp_verify.html'
    form_class = OTPCodeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        input_otp = form.cleaned_data['otp']
        session_otp = self.request.session.get('otp')
        phone = self.request.session.get('phone')

        if not session_otp or not phone:
            form.add_error(None, 'Session expired. Please request a new OTP.')
            return self.form_invalid(form)

        if input_otp == session_otp:
            user = User.objects.get(phone_number=phone)
            login(self.request, user)
            for key in ['otp','phone']:
                if key in self.request.session:
                    del self.request.session[key]
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid OTP.')
            return self.form_invalid(form)

class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('email_login')
    # template_name = 'register.html'
    #
    # def get(self,request):
    #     form = UserRegisterForm()
    #     return render(request,self.template_name,{'form':form})
    #
    # def post(self,request):
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         print("form is valid")
    #         form.save()
    #         messages.success(request, 'Registration successful. You can now log in.')
    #
    #         return redirect('email_login')
    #     else :
    #         return HttpResponseBadRequest()



class DashboardUserView(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        if user.role == "customer":
            comments = Comment.objects.filter(user=user)
            context = {"user":user,"comments":comments}
            return render(request, "customer_panel.html", context=context)
        elif user.role == "admin" or user.role=="manager" or user.role=="operator":
            store_products = Product.objects.filter(store=user)
            context = {"user":user,"products":store_products}
            return render(request, "vendor_panel.html", context=context)

        else :
            return HttpResponseForbidden()


class UpdateUserView(LoginRequiredMixin,UpdateView):
    login_url = 'login'
    model = User 
    form_class = UserRegisterForm  
    template_name = 'update_user.html'  
    success_url = reverse_lazy('dashboard_user')

    def form_valid(self, form):  
        messages.success(self.request, 'Item successfully updated!')  
        return super().form_valid(form)
    
# class CustomLogoutView(LoginRequiredMixin,LogoutView):
#     http_method_names = ["post", "options"]
#     template_name = 'logout.html'
#     next_page = 'home'

class CustomLogoutView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        logout(request)
        return redirect('home')

    # def post(self, request, *args, **kwargs):
    #     """Handle POST request for logout."""
    #     self.dispatch(request, *args, **kwargs)
    #     return super().post(request, *args, **kwargs)

class StoresList(View):
    template_name = 'stores_list.html'
    def get(self, request):
        stores = User.objects.filter(role="admin")
        context = {"stores":stores}
        return render(request,self.template_name, context=context)


class StoresDetail(View):
    template_name = 'stores_detail.html'
    def get(self, request,*args,**kwargs):
        store = User.objects.get(id=kwargs['id'],role="admin")
        products = Product.objects.filter(store=store)
        context = {"store":store,'products':products}
        return render(request,self.template_name, context=context)







