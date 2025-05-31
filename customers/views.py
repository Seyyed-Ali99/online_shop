# from django.contrib.auth.handlers.modwsgi import check_password
import decouple
from django.contrib.auth.hashers import check_password
from django.shortcuts import render,redirect
from django.http import HttpResponse , HttpResponseBadRequest,HttpResponseForbidden
from accounts.models import User
from product.models import Product,Comment
from .forms import UserRegisterForm, EmailLoginForm, OTPPhoneForm,StaffForm,UpdateUserForm,AdminCustomerRegisterForm,AddStaffForm
from django.contrib.auth.views import LogoutView , LoginView
from django.views import View
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import OTPPhoneForm,OTPCodeForm
import random
from kavenegar import *

# Create your views here.


class EmailLoginView(View):
    template_name = 'email_login.html'

    def get(self, request):
        form = EmailLoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EmailLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate( username=username, password=password)


            if user:
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
    form_class = AdminCustomerRegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('email_login')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # pass request to form for role logic
        return kwargs

    # def form_valid(self, form):
    #     user = form.save(commit=False)
    #     user.set_password(form.cleaned_data['password'])
    #     store = form.cleaned_data.get('store')
    #     if store:
    #         user.store = store
    #     user.save()
    #     login(self.request, user)
    #     return super().form_valid(form)


class DashboardUserView(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request,*args,**kwargs):
        user = User.objects.get(id=request.user.id)
        if user.role == "customer":
            # comments = Comment.objects.filter(user=user)
            context = {"user":user}
            return render(request, "customer_panel.html", context=context)
        elif user.role == "admin" or user.role=="manager" or user.role=="operator":
            # store_products = Product.objects.filter(store=user)
            context = {"user":user}
            return render(request, "vendor_panel.html", context=context)

        else :
            return HttpResponseForbidden()


class UpdateUserView(LoginRequiredMixin,UpdateView):
    login_url = 'email_login'
    model = User 
    form_class = UpdateUserForm
    template_name = 'update_user.html'  
    success_url = reverse_lazy('dashboard_user')

    def get_object(self, queryset=None):
        return self.request.user


class CustomLogoutView(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        logout(request)
        return redirect('home')


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

class StoresProducts(View):
    template_name = 'store_products.html'
    def get(self, request,*args,**kwargs):
        store = User.objects.get(id=kwargs['id'])
        products = Product.objects.filter(store=store)
        return render(request,self.template_name, context={'products':products})


class ShopProducts(View):
    template_name = 'shop_products.html'
    def get(self, request,*args,**kwargs):
        current_user = self.request.user
        if self.request.user.role == "manager" or self.request.user.role == "operator":
            product = Product.objects.filter(store=current_user.store)
            return render(request,self.template_name, context={'products':product})
        elif self.request.user.role == "admin":
            product = Product.objects.filter(store=current_user.id)
            return render(request,self.template_name, context={'products':product})
        else:
            return HttpResponseForbidden()


class StaffList(View):
    def get(self,request,*args,**kwargs):
        current_user = self.request.user
        if self.request.user.role == "admin":
            staff = User.objects.filter(store=current_user.id)
            return render(request,"staff_list.html",context={'staffs':staff })
        elif self.request.user.role == "manager" or self.request.user.role == "operator":
            staff = User.objects.filter(store=current_user.store)
            return render(request,"staff_list.html",context={'staffs':staff})
        else:
            return HttpResponseForbidden()

class StaffDetail(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self,request,*args,**kwargs):
        current_user = self.request.user
        user = User.objects.get(id=kwargs['id'])
        return render(request,"staff_detail.html",context={'user':user,'current_user':current_user})

class StaffUpdate(LoginRequiredMixin,UpdateView):
    login_url = 'email_login'
    model = User
    form_class = StaffForm
    template_name = 'staff_update.html'
    success_url = reverse_lazy('staff_list')

class DeleteStaff(LoginRequiredMixin,DeleteView):
    model = User
    success_url = reverse_lazy('staff_list')
    template_name = 'delete_staff.html'

class AddStaff(LoginRequiredMixin,CreateView):
    model = User
    form_class = AddStaffForm
    template_name = 'register.html'
    success_url = reverse_lazy('staff_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request  # pass request to form for role logic
        return kwargs

