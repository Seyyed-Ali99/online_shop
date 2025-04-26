from django.urls import path
from .views import HomePageView,Shop,Shop_Single
urlpatterns =[
    path('',HomePageView.as_view(),name='home' ),
    path('shop/',Shop.as_view(),name='shop' ),
    path('shop-single/',Shop_Single.as_view(),name='shop-single' ),
]