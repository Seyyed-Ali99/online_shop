from django.contrib import admin
from .models import Order
# Register your models here.
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id","date_of_deliver","total_price")
    list_filter = ("customer_id","date_of_deliver")