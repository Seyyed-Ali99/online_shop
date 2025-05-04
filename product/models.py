from django.db import models
from django.db.models import PositiveIntegerField

from accounts.models import User


# RATE_CHOICES = [("*","*"),("**","**"),("***","***"),("****","****"),("*****","*****")]

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    upper_category = models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150,blank=False,null=False)
    date_of_product = models.DateField(auto_now=True)
    image = models.FileField()
    category = models.ForeignKey(Category,on_delete=models.DO_NOTHING)
    amount = models.IntegerField(blank=False,null=False)
    store = models.ManyToManyField(User,related_name="Product")
    price = models.DecimalField(max_digits=10,decimal_places=2)


    def __str__(self):
        return f"{self.name} | {self.date_of_product} | {self.category.name} | {self.store.name} | {self.price}"


class Comment(models.Model):
    title = models.CharField(max_length=150,blank=False,null=False)
    comment_body = models.TextField()
    related_product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=False,null=False,default=None,related_name='Comment')

    def __str__(self):
        return f"{self.title} | {self.related_product.name} | {self.user.username}"

class Rate(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=False,null=False)
    user = models.ForeignKey(User,on_delete=models.DO_NOTHING,blank=False,null=False)
    rate = PositiveIntegerField(max_length=1,blank=False,null=False)

    def __str__(self):
        return f"{self.product} | {self.rate} | {self.user}"