from django.db import models
from accounts.models import User
from product.models import Product


class Order(models.Model):
    customer_id = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    product_id = models.ManyToManyField(Product,related_name="Order")
    address = models.CharField(max_length=250,blank=False,null=False)  
    date_of_deliver = models.DateField()
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.IntegerField()


    




