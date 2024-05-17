from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class ImageCategory(models.Model):
    """Модель для хранения изображений прадукта"""
    class Meta:
        verbose_name = "Image_category"
        verbose_name_plural = "Images_categories"

    src = models.ImageField(
        upload_to="category_image/",
        default="default.png",
        verbose_name="Link",
        blank=True,
        null=True,
    )
    alt = models.CharField(max_length=128, blank=True, null=True, verbose_name="Description")

    def __str__(self):
        return self.alt


class SubCategory(models.Model):
    """Модель для хранения подкатегорий прадукта"""

    title = models.CharField(max_length=255)
    image = models.ForeignKey(ImageCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    # parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    def __str__(self):
        return self.title


class Category(models.Model):
    """Модель для хранения категорий прадукта"""

    title = models.CharField(max_length=255, verbose_name="Title")
    image = models.ForeignKey(
        ImageCategory,
        on_delete=models.CASCADE,
        related_name="categories",
        verbose_name="Image_category"
    )
    subcategories = models.ManyToManyField(
        SubCategory,
        'self',
        blank=True,
        symmetrical=False,
        verbose_name="Subcategories"
    )

    def __str__(self):
        return self.title


class Product(models.Model):
    """Модель для хранения прадукта"""

    id = models.AutoField(primary_key=True, verbose_name="ID")
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, verbose_name="Category")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    count = models.PositiveIntegerField(verbose_name="Count")
    date = models.DateTimeField(verbose_name="Date")
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    fullDescription = models.TextField(blank=True, null=True, verbose_name="FullDescription")
    freeDelivery = models.BooleanField(default=False, verbose_name="FreeDelivery")
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, default=0.0, verbose_name="Rating")
    available = models.BooleanField(default=True)
    limited_edition = models.BooleanField(default=False)
    sort_index = models.IntegerField(blank=True, null=True,)
    sales_count = models.IntegerField(blank=True, null=True,)

    @classmethod
    def top_products(cls, limit):
        """
        Возвращает первые `limit` товаров, отсортированных по sort_index и sales_count.
        """
        return cls.objects.order_by('sort_index', '-sales_count')[:limit]

    def serialize(self):
        """
        Сериализует объект Product в словарь со всей актуальной информацией о продукте.
        """
        return {
            'id': self.id,
            'category': self.category.serialize(),  # Asigurați-vă că și categoria este serializată corespunzător
        }
    def __str__(self):
        return self.title


class Image(models.Model):
    """Модель для хранения изображений прадукта"""
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    src = models.ImageField(
        upload_to="product_image/",
        default="default.png",
        verbose_name="Link",
        blank=True,
        null=True,
    )
    alt = models.CharField(max_length=128, blank=True, null=True, verbose_name="Description")
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)

    def __str__(self):
        return self.alt


class Tag(models.Model):
    """Модель для хранения тагов прадукта"""
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    tag_id = models.AutoField(primary_key=True, verbose_name="Tag_ID")
    name = models.CharField(max_length=50, blank=True, verbose_name="Name")
    product = models.ManyToManyField(Product, related_name='tags', blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель для хранения  отзывов прадукта"""
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    author = models.CharField(max_length=255, blank=True, null=True, verbose_name="Author")
    email = models.EmailField(unique=True, blank=True, null=True, verbose_name="Email")
    text = models.TextField(blank=True, null=True, verbose_name="Text")
    rate = models.PositiveSmallIntegerField(blank=True, null=True, validators=[MinValueValidator(1),
                                            MaxValueValidator(5)], default=1, verbose_name="Rating")
    date = models.DateTimeField(blank=True, null=True, verbose_name="Date")
    product = models.ForeignKey(Product, blank=True, null=True, related_name='reviews', on_delete=models.CASCADE)

    def __str__(self):
        return f"Review for {self.product}: {self.author}"


class Specification(models.Model):
    """Модель для хранения спецификаций прадукта"""
    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    name = models.CharField(max_length=100, verbose_name="Name")
    value = models.CharField(max_length=255, verbose_name="Value")
    product = models.ManyToManyField(Product, related_name='specifications', blank=True)

    def __str__(self):
        return f"Specification for {self.product}: {self.name}, {self.value}"


class Sale(models.Model):
    """
    Модель для информации о продажах.
    """
    id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    salePrice = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Sale Price")
    dateFrom = models.DateField(verbose_name="Sale Start Date")
    dateTo = models.DateField(verbose_name="Sale End Date")
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales', verbose_name="Product")  # Conexiune la produsul vândut
    product_image = models.ForeignKey(Image, on_delete=models.CASCADE, verbose_name="Product Image")

    def __str__(self):
        return f"Sale for {self.product.title}"


class CartItem(models.Model):
    """
    Модель для элемента корзины.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.count} x {self.product.title}"


class Banner(models.Model):
    """
    Модель для баннера.
    """
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

