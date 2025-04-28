from django.contrib.auth.views import LoginView
from django.urls import path
from .views import EmailLoginView ,OTPLogin, RegisterView , UpdateUserView , DashboardUserView , CustomLogoutView

urlpatterns = [
    path("register/",RegisterView.as_view(),name='register'),
    path("email_login/",EmailLoginView.as_view(),name='email_login'),
    path("otp_login/",OTPLogin.as_view(),name='otp_login'),
    path("edit_user/",UpdateUserView.as_view(),name='update_user'),
    path("logout/",CustomLogoutView.as_view(),name='logout'),
    path("dashboard_user/<int:id>",DashboardUserView.as_view(),name='dashboard_user'),
    # path("vendor_dashboard/<int:id>",DashboardVendorView.as_view(),name='vendor_dashboard'),
    #
]