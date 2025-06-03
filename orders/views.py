# from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import datetime
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden

from .forms import PayForm, OrderUpdateForm
from .models import Order, OrderItem
from product.models import Product
from accounts.models import User
from .serializers import OrderSerializer


class CartView(APIView):
    def post(self,request,*args,**kwargs):
        product_id = request.data.get('product_id')
        # product_id = Product.objects.get(id=kwargs['id'])
        related_product = Product.objects.get(id=product_id)
        quantity = 1
        cart = request.session.get('cart', {})
        if quantity < related_product.amount:
            if str(product_id) in cart:
                cart[str(product_id)]['quantity'] += quantity
                print("adding amount to cart")

            else:
                cart[str(product_id)] = {'quantity': quantity}
                print("adding product to cart")


            request.session['cart'] = cart
            # print(cart)
            # print(related_product.amount)
            return Response({'message': 'Product added', 'cart': cart})
        else:
            return Response({'message': 'Product is out of stock'})




    # def post(self, request, *args, **kwargs):
    #     # product_id =str(request.data.get('product_id'))
    #     product_id = Product.objects.get(id=kwargs['id'])
    #     print(type(product_id))
    #     quantity = 1
    #     # product = Product.objects.get(id=int(product_id))
    #     cart = request.session.get('cart', {})
    #     for product in cart:
    #         if quantity > product_id.amount:
    #             if product in cart:
    #                 cart[product] += quantity # Increase quantity
    #                 product_id.amount -= 1
    #
    #             else:
    #                 cart[product] = quantity # Add new product
    #                 product_id.amount -= 1
    #
    #         else :
    #             return redirect('shop')
    #
    #     # Save cart in session
    #     request.session['cart'] = cart
    #     return JsonResponse(cart, safe=False, status=status.HTTP_201_CREATED)


    # Create your views here.

class DeleteCartItems(APIView):
    def delete(self, request):
        product_id = request.data.get(str('product_id'))

        cart = request.session.get('cart', {})
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart

        return JsonResponse(cart, safe=False)

class ShowCartItems(APIView):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})  # {'product_id': quantity, ...}
        products_list = []

        for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'image': product.image.url,
                    'category': product.category.name,
                    'amount': product.amount,
                    # 'store': product.store.username,
                    'date_of_product': str(product.date_of_product),
                    'price': str(product.price),
                    'quantity': quantity,
                })

        return Response({'products': products_list})
        # def get(self, request, *args, **kwargs):
        #     cart = request.session.get('cart', {})
        #     products_list = []
        #     for product in cart.keys() :
        #         product = Product.objects.get(id=product)
        #         products_list.append(product)
        #
        #     print(products_list)
        #     return Response(products_list)

class OrderCreateView(View):
    def get(self, request, *args, **kwargs):
        cart = request.session.get('cart', {})  # {'product_id': quantity, ...}
        products_list = []
        quantity = 0

        for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                quantity = quantity
                products_list.append({
                    'id': product.id,
                    'name': product.name,
                    'image': product.image.url,
                    'category': product.category.name,
                    'amount': product.amount,
                    'date_of_product': str(product.date_of_product),
                    'price': str(product.price),

                })
        # print(cart)
        return render(request,'show_order_products.html',{'products': products_list,'quantity':quantity})
    # @login_required(login_url='email_login')
    def post(self, request):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        if hasattr(request.user, 'role') and request.user.role == 'customer':
            cart = request.session.get('cart', {})
            prices = 0
            if not cart:
                return HttpResponse("No product available in cart!")


            customer = User.objects.get(id=request.user.id)
            # Create an order
            order = Order.objects.create(customer_id=customer, address=request.user.address, discount=1 )

            for product_id, quantity in cart.items():
                try:
                    product = Product.objects.get(id=product_id)
                    quan_dict = cart[str(product_id)]
                    quantity = quan_dict.get('quantity')
                    order_item = OrderItem.objects.create(
                        order=order,
                        product_id=product,
                        amount=quantity,
                        total_price=product.price * quantity
                    )
                    prices += order_item.total_price  # should use total_price, not `order_item.price`
                except Product.DoesNotExist:
                    continue  # ignore missing products

            order.total_price = prices
            order.save()

            del request.session['cart']
            return redirect('order_list')
        else:
            return HttpResponseForbidden()



class OrderListView(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self, request):
        # Retrieve all orders for the current user (you might want to filter by user)
        orders = Order.objects.filter(customer_id=self.request.user).order_by('-id') # Change to filter orders by user if necessary
        return render(request, 'orders_list.html', {'orders': orders})


class OrderDetailView(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(id=kwargs['id'])
        order_items = OrderItem.objects.filter(order=order)
        # products = Product.objects.filter(id=order_items.product_id)
        total_price = 0
        for order_item in order_items:
            total_price += order_item.product_id.price * order_item.amount

        order.total_price = total_price
        return render(request,"order_detail.html",context={'order': order,'order_items': order_items})

class ShopOrders(LoginRequiredMixin,View):
    login_url = 'email_login'
    def get(self, request):
        current_user = self.request.user
        if current_user.role == 'admin':
            orders = Order.objects.filter(order_items__product_id__store=current_user.id).order_by('-id')
            # serializer = OrderSerializer(orders, many=True)
            return render(request,'store_orders.html',context={'orders': orders})
        elif current_user.role == 'operator' or current_user.role == 'manager':
            orders = Order.objects.filter(order_items__product_id__store=current_user.store.id).order_by('-id')
            # serializer = OrderSerializer(orders, many=True)
            return render(request,'store_orders.html',context={'orders': orders})
        else:
            return HttpResponseForbidden()


# class Purchase(LoginRequiredMixin,UpdateView):
#     login_url = 'email_login'
#     template_name = 'order_detail.html'
#     model = Order
#     form_class = PayForm
#     success_url = reverse_lazy('order_list')

class OrderUpdateView(LoginRequiredMixin,UpdateView):
    login_url = 'email_login'
    form_class = OrderUpdateForm
    model = Order
    template_name = 'order_update.html'
    success_url = reverse_lazy('shop_orders')

# class CustomerOrders(APIView):
#     permission_classes = [IsAuthenticated]
#     login_url = 'email_login'
#     def get(self, request):
#         current_user = self.request.user
#         orders = Order.objects.filter(order_items__customer_id=current_user.id).order_by('-id')
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)




# class OrderUpdateView(LoginRequiredMixin,UpdateView):
#     model = Order
#     form_class = UserRegisterForm
#     template_name = 'update_user.html'
#     success_url = reverse_lazy('dashboard')  # Redirect to dashboard after update
#
#     def form_valid(self, form):
#         messages.success(self.request, 'Item successfully updated!')
#         return super().form_valid(form)

# class OrderUpdateView(APIView):
#     model = Order
#     template_name = 'order_update.html'
#     fields = ["date_of_deliver","discount","address","orderitem_id"]
#     success_url = reverse_lazy('order_list')




