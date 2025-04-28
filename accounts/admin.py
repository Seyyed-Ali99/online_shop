from django.contrib import admin
from .models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username","email","role")
    list_filter = ("username","email","role","phone_number")
    search_fields = ("last_name__startswith","first_name__startswith","username__startswith")
