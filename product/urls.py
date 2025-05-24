from django.urls import path
from .views import AddCategory, AddProduct, AddComment, ProductUpdate, ProductList, ProductDetail, ProductDelete,CommentList

urlpatterns = [
    path('product/<int:id>/add_comment/', AddComment.as_view(), name='add_comment'),
    path('add_product/', AddProduct.as_view(), name='add_product'),

    path("all_comments/",CommentList.as_view(),name="comments_list"),

    path("product/<int:pk>/edit/",ProductUpdate.as_view(),name="edit_product"),
    path("shop/",ProductList.as_view(),name="shop"),
    path("product/<int:id>/",ProductDetail.as_view(),name="product_detail"),
    path("product_delete/<int:id>/",ProductDelete.as_view(),name="product_delete"),
]