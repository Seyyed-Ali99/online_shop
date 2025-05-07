from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from rest_framework.generics import RetrieveAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views import View
from django.http import JsonResponse
from .models import Order, OrderItem
from product.models import Product
from django.views.generic import UpdateView
from .serializers import OrderItemSerializer,OrderSerializer


class CartView(APIView):


    def post(self, request):
        product_id =str(request.data.get('product_id'))
        print(type(product_id))
        # quantity = request.data.get('quantity', 1)
        quantity = 1
        product = Product.objects.get(id=int(product_id))
        cart = request.session.get('cart', {})
        for product in cart:
            print(product)
        if quantity > product.amount:
            if product_id in cart:
                cart[product_id] += quantity # Increase quantity
                product.amount -= 1
                print(cart)
            else:
                cart[product_id] = quantity # Add new product
                product.amount -= 1
                print(cart)
        else :
            return redirect('shop')

        # Save cart in session
        request.session['cart'] = cart
        return JsonResponse(cart, safe=False, status=status.HTTP_201_CREATED)


    # Create your views here.

class DeleteCartItems(APIView):
    def delete(self, request):
        product_id = request.data.get(str('product_id'))


        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return JsonResponse(cart, safe=False)

class ShowCartItems(RetrieveAPIView):

        renderer_classes = [TemplateHTMLRenderer]

        def get(self, request, *args, **kwargs):
            cart = request.session.get('cart', {})
            products_list = []
            for product in cart.keys() :
                product = Product.objects.get(id=product)
                products_list.append(product)

            return Response({'products': products_list}, template_name='cart.html')

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
                OrderItem.objects.create(order=order, product=product, amount=quantity)
            except:
                continue  # Ignore if the product doesn't exist, or handle it

        # Clear the cart after creating an order
        del request.session['cart']

        return redirect('order_list')


class OrderListView(APIView):
    login_url = 'email_login'
    def get(self, request):
        # Retrieve all orders for the current user (you might want to filter by user)
        orders = Order.objects.filter(customer_id=self.request.user) # Change to filter orders by user if necessary
        return render(request, 'orders_list.html', {'orders': orders})


class OrderDetailView(APIView):
    login_url = 'email_login'
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        total_price = 0
        for order_item in order_items:
            total_price += order_item.product.price * order_item.quantity

        order.total_price = total_price
        return render(request,"order_detail.html",context={'order': order,'order_items': order_items})


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


