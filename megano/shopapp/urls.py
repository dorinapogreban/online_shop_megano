from django.urls import path
from .views import (
    ProductDetailView,
    ProductReviewCreateView,
    TagListView,
    TagDetailView

)


"""
Настраиваем маршруты URL, чтобы можно было обращаться к представлению для регистрации через API.
"""
app_name = "shopapp"

urlpatterns = [
    path("product/<int:id>", ProductDetailView.as_view(), name="product-details"),
    path("product/<int:id>/review", ProductReviewCreateView.as_view(), name="product-review"),
    path('tags', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>', TagDetailView.as_view(), name='tag-detail'),
]