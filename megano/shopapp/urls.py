from django.urls import path
from .views import (
    ProductDetailView,
    ProductReviewCreateView,
    TagListView,
    TagDetailView,
    CategoryAPIView,
    CatalogAPIView,
    PopularProductsAPIView,
    LimitedProductsAPIView,
    SaleAPIView,
    CartAPIView,
    BannerList,

)


"""
Настраиваем маршруты URL, чтобы можно было обращаться к представлению для регистрации через API.
"""
app_name = "shopapp"

urlpatterns = [
    path("product/<int:id>", ProductDetailView.as_view(), name="product-details"),
    path("product/<int:id>/reviews", ProductReviewCreateView.as_view(), name="product-review"),
    path('tags', TagListView.as_view(), name='tag-list'),
    path('tags/<int:pk>', TagDetailView.as_view(), name='tag-detail'),
    path('basket', CartAPIView.as_view(), name='basket'),
    path('categories', CategoryAPIView.as_view(), name='categories'),
    path('catalog', CatalogAPIView.as_view(), name='catalog'),
    path('products/popular', PopularProductsAPIView.as_view(), name='products-popular'),
    path('products/limited', LimitedProductsAPIView.as_view(), name='products-limited'),
    path('sales', SaleAPIView.as_view(), name='sale'),
    path('banners', BannerList.as_view(), name='banners'),

]