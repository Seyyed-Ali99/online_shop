from django.urls import path
from .views import CartView, OrderCreateView, OrderListView, OrderDetailView, ShowCartItems, \
    DeleteCartItems, ShopOrders, CustomerOrders

urlpatterns = [
    path('api/cart/add/', CartView.as_view(), name='cart'),

    path('api/cart/<int:product_id>/delete/', DeleteCartItems.as_view(), name='cart_delete'),

    path('api/show_cart/',ShowCartItems.as_view(),name='cart_items'),
    # path('update/', OrderUpdateView.as_view(), name='update_order'), # currently unavailable
    path('add_order/', OrderCreateView.as_view(), name='add_order'),
    path('shop_orders/', ShopOrders.as_view(),name='shop_orders'),
    path('customer_orders/', CustomerOrders.as_view(),name='customer_orders'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('order', OrderUpdateView.as_view(), name='order_update'),
]