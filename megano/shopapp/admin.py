from django.contrib import admin
from .models import Product, Tag, Review, Image, Specification


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "description", 'fullDescription', "price", "rating",
                    "freeDelivery", "category", "count", "date")
    list_display_links = "pk", "title"
    # ordering = "-title"
    search_fields = "title", "description", "price", "rating", "freeDelivery", "category"
    def description_short(self, obj: Product) ->str:
        if len(obj.description) < 48:
            return obj.description
        return obj.description[:48] + "..."


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['author', 'email', 'text', 'rate', 'date', 'product']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['src', 'alt', 'product']


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'value', 'product']