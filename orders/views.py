from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse


class CartView(APIView):
    def get(self, request):

        cart = request.session.get('cart', {})
        return JsonResponse(cart, safe=False)

    def post(self, request):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)


        cart = request.session.get('cart', {})


        if product_id in cart:
            cart[product_id] += quantity  # Increase quantity
        else:
            cart[product_id] = quantity  # Add new product

        # Save cart in session
        request.session['cart'] = cart
        return JsonResponse(cart, safe=False, status=status.HTTP_201_CREATED)

    def delete(self, request):
        product_id = request.data.get('product_id')

        # Remove product from cart
        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return JsonResponse(cart, safe=False)
    # Create your views here.


