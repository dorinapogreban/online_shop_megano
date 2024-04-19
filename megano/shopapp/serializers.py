from rest_framework import serializers
from .models import Product, Image, Tag, Specification, Review


class ImageSerializer(serializers.ModelSerializer):
    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Image
        fields = ['src', 'alt']

    def get_src(self, obj):
        return obj.src.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag_id', 'name']


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['name', 'value']


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()  # Adăugăm un câmp pentru a prelua product_id

    class Meta:
        model = Review
        fields = ['author', 'email', 'text', 'rate', 'date', 'product_id']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')  # Extragem product_id din datele validate
        review = Review.objects.create(product_id=product_id, **validated_data)  # Creăm recenzia cu product_id
        return review


class ProductSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription',
                  'freeDelivery', 'images', 'tags', 'reviews', 'specifications', 'rating',]

