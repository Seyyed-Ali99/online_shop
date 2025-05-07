from djcelery.utils import now_localtime
from rest_framework import serializers

from accounts.models import User
from product.models import Product
from .models import Order,OrderItem

# class CartItemSerializer(serializers.Serializer):
#         product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#         user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#         created_at = serializers.DateTimeField()


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = '__all__'



