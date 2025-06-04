from django import forms
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order

class PayForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_paid']


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['is_paid','status','date_of_deliver','discount']


