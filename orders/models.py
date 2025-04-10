from django.db import models
from accounts.models import Customer,Vendor,Store_owner
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    upper_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

class Product(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    date_of_product = models.DateField(auto_now=True)
    image = models.FileField()
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    amount = models.IntegerField(blank=False,null=False)
    store = models.ManyToManyField(Store_owner,related_name="Product")

class Order(models.Model):
    customer_id = models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    product_id = models.ManyToManyField(Product,related_name="Order")
    address = models.CharField(max_length=250,blank=False,null=False)  
    date_of_deliver = models.DateField()
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.IntegerField()

class Comment(models.Model):
    title = models.CharField(max_length=150,blank=False,null=False)
    comment_body = models.TextField()
    related_product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False,null=False)

    




