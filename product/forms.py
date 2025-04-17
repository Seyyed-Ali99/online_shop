from django import forms
from .models import Category , Product , Comment

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"