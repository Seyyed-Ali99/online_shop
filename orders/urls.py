from django.urls import path
from .views import CartView, OrderUpdateView, OrderCreateView, OrderListView, OrderDetailView

urlpatterns = [
    path('api/cart/', CartView.as_view(), name='cart'),
    path('update/', OrderUpdateView.as_view(), name='update_order'),
    path('add_order/', OrderCreateView.as_view(), name='add_order'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('order', OrderUpdateView.as_view(), name='order_update'),
]