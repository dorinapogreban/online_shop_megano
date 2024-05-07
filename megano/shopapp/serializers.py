from rest_framework import serializers
from .models import Product, Image, Tag, Specification, Review, Category, ImageCategory, SubCategory, Sale


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений продукта.

    Позволяет получить сериализованное представление изображения продукта с ссылкой на изображение.
    """

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Image
        fields = ['src', 'alt']

    def get_src(self, obj):
        """
        Получение ссылки на изображение.
        Args:
            obj: Объект изображения.
        Returns:
            str: Ссылка на изображение.
        """
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


class ImageCategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений категорий и подкатегорий"""

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = ImageCategory
        fields = ['src', 'alt']

    def get_src(self, obj):
        return obj.src.url


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для получения подкатегорий"""

    image = ImageCategorySerializer()

    class Meta:
        model = SubCategory
        fields = ['id', 'title', 'image']


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для получения категорий"""

    image = ImageCategorySerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')

    def get_subcategories(self, obj):
        """
        Получение данных о подкатегориях.
        Args:
           obj: Объект категории.
        Returns:
           list: Список данных о подкатегориях.
        """
        subcategories = obj.subcategories.all()
        subcategories_data = []
        for subcategory in subcategories:
            subcategory_data = {
                'id': subcategory.id,
                'title': subcategory.title,
                'image': {
                    'src': subcategory.image.src.url,
                    'alt': subcategory.image.alt
                }
            }
            subcategories_data.append(subcategory_data)
        return subcategories_data


class SaleProductSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')  # Accesăm câmpul 'title' din modelul 'Product'
    product_image = serializers.CharField(source='product.images.first.src')  # Accesăm prima imagine asociată produsului

    class Meta:
        model = Sale
        fields = ['id', 'price', 'salePrice', 'dateFrom', 'dateTo', 'product_title', 'product_image']
