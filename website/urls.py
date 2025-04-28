from django.urls import path
from .views import HomePageView,Shop,ShopSingle
urlpatterns =[
    path('',HomePageView.as_view(),name='home' ),
    path('shop/',Shop.as_view(),name='shop' ),
    path('shop-single/',ShopSingle.as_view(),name='shop-single' ),
]