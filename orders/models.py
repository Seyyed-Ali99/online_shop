from django.db import models
from accounts.models import User
from product.models import Product


class Order(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None,blank=False,null=False)
    # orderitem_id = models.ForeignKey(OrderItem,related_name="Order",on_delete=models.DO_NOTHING,default=1)
    address = models.CharField(max_length=250,blank=False,null=False)  
    date_of_deliver = models.DateField(blank=False,null=False)
    total_price = models.DecimalField(max_digits=10,decimal_places=2, blank=False,null=False)
    discount = models.IntegerField()
    is_paid = models.BooleanField(blank=False,null=False,default=False)

    def __str__(self):
        return f"{self.customer_id} - {self.date_of_deliver} - {self.total_price} - {self.discount} - {self.is_paid} "

class OrderItem(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.DO_NOTHING,default=1)
    amount = models.IntegerField(blank=False,null=False,default=1)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    order = models.ForeignKey(Order,on_delete=models.DO_NOTHING,default=1,related_name='order_items')

    def __str__(self):
        return f"{self.product_id} - {self.amount} - {self.total_price} - {self.order}"

# class Cart(models.Model):
#     # cart_item = models.ForeignKey(CartItem,on_delete=models.DO_NOTHING,default=None , related_name='Cart')
#     total_price = models.DecimalField(max_digits=10,decimal_places=2)
#
# class CartItem(models.Model):
#     product_id = models.ForeignKey(Product,on_delete=models.DO_NOTHING,default=None , related_name='CartItem')
#     amount = models.IntegerField(blank=False,null=False,default=1)
#     price = models.DecimalField(max_digits=10,decimal_places=2)
#     cart = models.ForeignKey(Cart,on_delete=models.DO_NOTHING,default=1,related_name='CartItem',blank=False,null=False)
#

    




