from rest_framework import serializers
from .models import Product, Image, Tag, Specification, Review


class ImageSerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений прадукта"""

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Image
        fields = ['src', 'alt']

    def get_src(self, obj):
        return obj.src.url


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тагов прадукта"""
    class Meta:
        model = Tag
        fields = ['tag_id', 'name']


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериалайзер для спецификаций прадукта"""
    class Meta:
        model = Specification
        fields = ['name', 'value']


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов прадукта. Доступ имеет только авторизованный пользователь."""
    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate']


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и/или обнавления прадукта."""

    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription',
                  'freeDelivery', 'images', 'tags', 'reviews', 'specifications', 'rating',]

