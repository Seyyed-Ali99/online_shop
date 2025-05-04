from django.urls import path
from .views import HomePageView,Shop,ShopSingle,About
urlpatterns =[
    path('',HomePageView.as_view(),name='home' ),
    # path('shop/',Shop.as_view(),name='shop' ),
    # path('shop-single/',ShopSingle.as_view(),name='shop-single' ),
    path('about/',About.as_view(),name='about' ),
]