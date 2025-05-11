from django.urls import path
from .views import HomePageView,Shop,ShopSingle,About,ContactUs,SearchHome
urlpatterns =[
    path('',HomePageView.as_view(),name='home' ),
    # path('shop/',Shop.as_view(),name='shop' ),
    # path('shop-single/',ShopSingle.as_view(),name='shop-single' ),
    path('about/',About.as_view(),name='about' ),
    path('contact/',ContactUs.as_view(),name='contact' ),
    path('search/',SearchHome.as_view(),name='search' ),
]