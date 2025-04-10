from django.contrib import admin
from accounts.models import Customer,Vendor,Store_owner
from orders.models import Category , Product , Order , Comment
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    pass

@admin.register(Store_owner)
class OwnerAdmin(admin.ModelAdmin):
    pass

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


