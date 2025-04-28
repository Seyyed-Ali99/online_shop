from django.contrib import admin
from .models import Order,OrderItem
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","date_of_deliver","is_paid","customer_id")
    list_filter = ("customer_id","date_of_deliver","is_paid")
    search_fields = ("customer_id__username","id")
    # inlines = [OrderItem]

@admin.register(OrderItem)
class OrderItem(admin.ModelAdmin):
    list_display = ("id","product_id","amount","order")
    list_filter =  ("product_id","order","total_price")
    search_fields = ("product_id__name","order__customer_id__username","id")
    # search_fields = ()
