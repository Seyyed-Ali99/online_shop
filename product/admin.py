from django.contrib import admin
from .models import Category , Product , Comment
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","category","date_of_product","amount","price")
    list_filter = ("name","category","price","date_of_product")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass    
   
