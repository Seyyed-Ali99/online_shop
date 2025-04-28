from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.http import JsonResponse
from .models import Order, OrderItem
from product.models import Product
from django.views.generic import UpdateView


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




class OrderCreateView(APIView):
    def post(self, request):
        # Get the cart from session
        cart = request.session.get('cart', {})

        if not cart:
            return JsonResponse({'error': 'Cart is empty.'}, status=400)

            # Create an order
        order = Order.objects.create()

        # Create order items based on the cart
        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
            except:
                continue  # Ignore if the product doesn't exist, or handle it accordingly

        # Clear the cart after creating an order
        del request.session['cart']

        return JsonResponse({'order_id': order.id}, status=201)


class OrderListView(APIView):
    def get(self, request):
        # Retrieve all orders for the current user (you might want to filter by user)
        orders = Order.objects.all()  # Change to filter orders by user if necessary
        return render(request, 'orders_list.html', {'orders': orders})


class OrderDetailView(APIView):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        return render(request,"order_detail.html",context={'order': order})


# class OrderUpdateView(LoginRequiredMixin,UpdateView):
#     model = Order
#     form_class = UserRegisterForm
#     template_name = 'update_user.html'
#     success_url = reverse_lazy('dashboard')  # Redirect to dashboard after update
#
#     def form_valid(self, form):
#         messages.success(self.request, 'Item successfully updated!')
#         return super().form_valid(form)

class OrderUpdateView(APIView):
    model = Order
    template_name = 'order_update.html'
    fields = ["date_of_deliver","discount","address","orderitem_id"]  # Specify fields you want to be editable
    success_url = reverse_lazy('order_list')  # Redirect after update

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['order'] = self.object  # Add the order instance to the context
    #     return context


