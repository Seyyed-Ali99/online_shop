from django.db import models
from accounts.models import User
from product.models import Product

class OrderItem(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.DO_NOTHING,default=1)
    amount = models.IntegerField(blank=False,null=False,default=1)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)

class Order(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    orderitem_id = models.ForeignKey(OrderItem,related_name="Order",on_delete=models.DO_NOTHING,default=1)
    address = models.CharField(max_length=250,blank=False,null=False)  
    date_of_deliver = models.DateField()
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.IntegerField()


    




