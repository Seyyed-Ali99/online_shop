from django.urls import path
from .views import AddCategory , AddProduct , AddComment , ProductUpdate , ProductList , ProductDetail

urlpatterns = [
    path("add_product/",AddProduct.as_view(),name="add_product"),
    path("add_category/",AddCategory.as_view(),name="add_category"),
    path("add_comment/",AddComment.as_view(),name="add_comment"),
    path("edit_product/",ProductUpdate.as_view(),name="edit_product"),
    path("all_products/",ProductList.as_view(),name="all_product"),
    path("product/<int:id>",ProductDetail.as_view(),name="product_detail"),
]