from django.db import models
from django.contrib.auth.models import AbstractUser, Group , Permission
# Create your models here.

ROLE_CHOICES = [('manager','manager'),('admin','admin'),('customer','customer'),('operator','operator')]
class User(AbstractUser):
    first_name = models.CharField(max_length=150,blank=False,null=False)
    last_name = models.CharField(max_length=150,blank=False,null=False)
    username = models.CharField(max_length=150,blank=False,null=False,unique=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11,blank=False,null=False,unique=True)
    password = models.CharField(max_length=150,blank=False,null=False)
    role = models.CharField(max_length=50,blank=False,null=False,choices=ROLE_CHOICES,default='operator')
    address = models.CharField(max_length=250)

    USERNAME_FIELD = 'email'
#   def __str__(self):
#       return f"{self.username} | {self.email} | {self.role}"

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="CustomeUser_set",
        related_query_name="customer",
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="customerpermissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="CustomeUser_set",
        related_query_name="customer",
    )
    
    
    def __str__(self):
        return f"{self.username} | {self.email} "

# class Vendor(Customer):
   
#     role = models.CharField(max_length=50,blank=False,null=False,choices=ROLE_CHOICES,default='operator')

#     def __str__(self):
#         return f"{self.username} | {self.email} | {self.role}"
    
# class Store_owner(Customer):
#     store_name = models.CharField(max_length=150,blank=False,null=False)
#     store_address = models.CharField(max_length=250,blank=False,null=False)  

# class Vendors(AbstractUser):


