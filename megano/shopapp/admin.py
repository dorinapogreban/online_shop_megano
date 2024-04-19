from django.contrib import admin
from .models import Product, Tag, Review


admin.site.register(Product)
admin.site.register(Tag)
admin.site.register(Review)


class ProductAdmin(admin.ModelAdmin):
    list_display = "pk", "title", "description", "price", "rating", "freeDelivery", "images"
    list_display_links = "pk", "title"


class TagAdmin(admin.ModelAdmin):
    list_display = ['name']
