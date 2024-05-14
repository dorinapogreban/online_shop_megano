from django.contrib import admin
from .models import (Product, Tag, Review, Image, Specification, Category, ImageCategory, SubCategory, Sale, CartItem,
                    Banner )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", 'fullDescription', "price", "rating",
                    "freeDelivery", "category", "count", "date")
    list_display_links = "pk", "title"
    list_filter = ["price", "rating", "category", "date", "count"]

    # ordering = "-title"
    search_fields = "title", "description", "price", "rating", "freeDelivery", "category"

    def description_short(self, obj: Product) ->str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    search_fields = ['name']



@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'email', 'text', 'rate', 'date', 'product']
    list_filter = ['date', 'product', 'author', 'rate']
    search_fields = ['text', 'email']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['src', 'alt', 'product']
    list_filter = ['product']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'product']
    list_filter = ['value', 'product']
    search_fields = ['name']


@admin.register(ImageCategory)
class ImageCategoryAdmin(admin.ModelAdmin):
    list_display = ['src', 'alt']


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']
    list_filter = ['image']
    search_fields = ['title']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'image']
    list_filter = ['image']
    search_fields = ['title']


@admin.register(Sale)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'product']
    list_filter = ['dateFrom', 'dateTo']
    search_fields = ['product__title']


@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'count']
    list_filter = ['count']
    search_fields = ['product']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['product']
