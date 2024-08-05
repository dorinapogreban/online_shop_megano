from rest_framework import serializers
from .models import (
    Product,
    Image,
    Tag,
    Specification,
    Review,
    Category,
    ImageCategory,
    SubCategory,
    Sale,
    CartItem,
    Banner,
)


class ImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений продукта.

    Позволяет получить сериализованное представление изображения продукта с ссылкой на изображение.
    """

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = Image
        fields = ["src", "alt"]

    # def get_src(self, obj):
    #     """
    #     Получение ссылки на изображение.
    #     Args:
    #         obj: Объект изображения.
    #     Returns:
    #         str: Ссылка на изображение.
    #     """
    #     return obj.src.url
    def get_src(self, obj):
        """
        Get the list of image URLs.
        Args:
            obj: Image object.
        Returns:
            list: List of image URLs.
        """
        # Assuming that Image model has a ForeignKey to a Product model.
        product_images = Image.objects.filter(product=obj.product)
        if product_images.exists():
            return product_images.first().src.url
        print(product_images)
        return None


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для тагов прадукта"""

    class Meta:
        model = Tag
        fields = ["tag_id", "name"]


class SpecificationSerializer(serializers.ModelSerializer):
    """Сериалайзер для спецификаций прадукта"""

    class Meta:
        model = Specification
        fields = ["name", "value"]


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов прадукта. Доступ имеет только авторизованный пользователь."""

    class Meta:
        model = Review
        fields = ["author", "email", "text", "rate"]


class ProductSerializer(serializers.ModelSerializer):
    """Сериалайзер для получения и/или обнавления прадукта."""

    # images = ImageSerializer(many=True)
    images = serializers.SerializerMethodField()

    tags = TagSerializer(many=True)
    reviews = ReviewSerializer(many=True)
    specifications = SpecificationSerializer(many=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "fullDescription",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "specifications",
            "rating",
        ]

    def get_images(self, obj):
        if obj.images.exists():
            return ImageSerializer(obj.images.all(), many=True).data
        else:
            return []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["images"] = self.get_images(instance)
        return data


class ImageCategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для изображений категорий и подкатегорий"""

    src = serializers.SerializerMethodField()  # тут возвращаем ссылку на изображение

    class Meta:
        model = ImageCategory
        fields = ["src", "alt"]

    def get_src(self, obj):
        return obj.src.url


class SubCategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для получения подкатегорий"""

    image = ImageCategorySerializer()

    class Meta:
        model = SubCategory
        fields = ["id", "title", "image"]


class CategorySerializer(serializers.ModelSerializer):
    """Сериалайзер для получения категорий"""

    image = ImageCategorySerializer()
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "title", "image", "subcategories")

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
                "id": subcategory.id,
                "title": subcategory.title,
                "image": {
                    "src": subcategory.image.src.url,
                    "alt": subcategory.image.alt,
                },
            }
            subcategories_data.append(subcategory_data)
        return subcategories_data


class SaleProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для продуктов, находящихся на распродаже.
    """

    title = serializers.CharField(
        source="product.title"
    )  # Доступ к полю 'title' модели 'Product'
    images = (
        serializers.SerializerMethodField()
    )  # Определяем поле 'images' как SerializerMethodField

    class Meta:
        model = Sale
        fields = ["id", "price", "salePrice", "dateFrom", "dateTo", "title", "images"]

    def get_images(self, obj):
        """
        Получает изображения продукта.
        """
        product = obj.product  # Получаем продукт, связанный с продажей
        images = product.images.all()  # Получаем все изображения, связанные с продуктом
        return ImageSerializer(
            images, many=True
        ).data  # Сериализует изображения и возвращает данные

    def to_representation(self, instance):
        """
        Преобразует экземпляр в представление.
        """
        representation = super().to_representation(instance)
        representation["images"] = self.get_images(
            instance
        )  # Заменяем поле 'images' в сериализованном представлении на изображения, связанные с продуктом
        return representation


class CartItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для элементов корзины.
    """

    class Meta:
        model = CartItem
        fields = ["id", "product", "count"]


class BannerSerializer(serializers.ModelSerializer):
    """
    Сериализатор для баннеров.
    """

    category = serializers.SerializerMethodField()
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.price"
    )
    count = serializers.IntegerField(source="product.count")
    date = serializers.DateTimeField(source="product.date")
    title = serializers.CharField(source="product.title")
    description = serializers.CharField(source="product.description")
    freeDelivery = serializers.BooleanField(source="product.freeDelivery")
    images = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    rating = serializers.DecimalField(
        max_digits=3, decimal_places=1, source="product.rating"
    )

    class Meta:
        model = Banner
        fields = [
            "id",
            "category",
            "price",
            "count",
            "date",
            "title",
            "description",
            "freeDelivery",
            "images",
            "tags",
            "reviews",
            "rating",
        ]

    def get_category(self, obj):
        """
        Получить идентификатор категории продукта.
        """
        return obj.product.category.id

    def get_images(self, obj):
        """
        Получить изображения продукта.
        """
        images = obj.product.images.all()
        return [{"src": image.src.url, "alt": image.alt} for image in images]

    def get_tags(self, obj):
        """
        Получить теги продукта.
        """
        tags = obj.product.tags.all()
        return [{"id": tag.pk, "name": tag.name} for tag in tags]

    def get_reviews(self, obj):
        """
        Получить количество отзывов о продукте.
        """
        return obj.product.reviews.count()
