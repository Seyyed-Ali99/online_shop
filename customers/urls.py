
from django.urls import path
from .views import EmailLoginView ,OTPLogin,OTPVerify, RegisterView , UpdateUserView , DashboardUserView , CustomLogoutView,StoresList,StoresDetail

urlpatterns = [
    path("register/",RegisterView.as_view(),name='register'),
    path("email_login/",EmailLoginView.as_view(),name='email_login'),
    path("otp_login/",OTPLogin.as_view(),name='otp_login'),
    path("otp_verify/",OTPVerify.as_view(),name='otp_verify'),
    path("logout/",CustomLogoutView.as_view(),name='logout'),

    path("edit_user/",UpdateUserView.as_view(),name='update_user'),
    path("dashboard_user/",DashboardUserView.as_view(),name='dashboard_user'),

    path("stores_list/",StoresList.as_view(),name='stores_list'),
    path("stores_detail/<int:id>",StoresDetail.as_view(),name='stores_detail'),
    # path("vendor_dashboard/<int:id>",DashboardVendorView.as_view(),name='vendor_dashboard'),
    #
]