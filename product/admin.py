from django.contrib import admin
from .models import Category , Product , Comment,Rate
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","upper_category")
    list_filter = ("name","upper_category__name")
    search_fields = ("name","upper_category__name")

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","category","date_of_product","amount","price")
    list_filter = ("name","category","price","date_of_product")
    search_fields = ("name","price","category__name")

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("title","related_product","user")
    list_filter = ("related_product","user")
    search_fields = ("related_product__name","user__username")


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rate")
    list_filter = ("product", "rate","user")
    search_fields = ("product__name", "user__username")
