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

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['title','comment_body','related_product','user']
        # exclude = ['user','related_product']
        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop('request', None)
        #     super().__init__(*args, **kwargs)
        #     self.fields['related_product'].queryset = Product.objects.get(id=kwargs['instance'].id)
        #     self.fields['user'].queryset = self.request.user
        #     # self.fields['related_product'].choices = []

        # def __init__(self, *args, **kwargs):
        #     self.request = kwargs.pop('request', None)
        #     self.related_product_instance = kwargs.pop('related_product', None)
        #
        #     super().__init__(*args, **kwargs)
        #
        #     # Optional: make these fields read-only/display-only if you add them back
        #     # but better to exclude them entirely from form fields.
        #
        # def save(self, commit=True):
        #     comment = super().save(commit=False)
        #     if self.request:
        #         comment.user = self.request.user
        #     if self.related_product_instance:
        #         comment.related_product = self.related_product_instance
        #     if commit:
        #         comment.save()
        #     return comment


class RateForm(forms.ModelForm):
    class Meta:
        model = Rate
        fields = "__all__"
