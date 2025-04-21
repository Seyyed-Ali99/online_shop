from django.urls import path
from .views import CustomeLoginView , RegisterView , UpdateUserView , DashboardUserView , CustomLogoutView

urlpatterns = [
    path("register/",RegisterView.as_view(),name='register'),
    path("login/",CustomeLoginView.as_view(),name='login'),
    path("edit_user/",UpdateUserView.as_view(),name='edit_user'),
    path("logout/",CustomLogoutView.as_view(),name='logout'),
    path("customer_dashboard/<int:id>",DashboardUserView.as_view(),name='user_dashboard'),
    # path("vendor_dashboard/<int:id>",DashboardVendorView.as_view(),name='vendor_dashboard'),
    #
]