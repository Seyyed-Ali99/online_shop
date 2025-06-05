from django import forms
from .models import Category , Product , Comment,Rate

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop('request', None)
        #     super().__init__(*args, **kwargs)
        #
        #     current_user = self.request.user
        #     if current_user.role == 'admin':
        #         self.fields['store'].initial = current_user.id
        #     else:
        #         self.fields['store'].initial = current_user.store.id
        #
        # def save(self, commit=True):
        #     product = super().save(commit=False)
        #     if commit:
        #         product.save()
        #     return product


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','comment_body','related_product','user']


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = "__all__"

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name','image','price','amount','category']
