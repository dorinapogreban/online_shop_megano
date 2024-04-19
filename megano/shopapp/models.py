from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# class Image(models.Model):
#     class Meta:
#         verbose_name = "Image"
#         verbose_name_plural = "Images"
#
#     src = models.ImageField(
#         upload_to="product_image/",
#         default="default.png",
#         verbose_name="Link",
#         blank=True,
#     )
#     alt = models.CharField(max_length=128, blank=True, verbose_name="Description")
#
#
# class Tag(models.Model):
#     class Meta:
#         verbose_name = "Tag"
#         verbose_name_plural = "Tags"
#
#     tag_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=50, blank=True)
#
#
# class Review(models.Model):
#     class Meta:
#         verbose_name = "Review"
#         verbose_name_plural = "Reviews"
#
#     author = models.CharField(max_length=255)
#     email = models.EmailField(unique=True, verbose_name="Email")
#     text = models.TextField()
#     rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     date = models.DateTimeField()
#     # product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
#
#
# class Specification(models.Model):
#     class Meta:
#         verbose_name = "Specification"
#         verbose_name_plural = "Specifications"
#
#     name = models.CharField(max_length=100)
#     value = models.CharField(max_length=255)


# class Product(models.Model):
#     """Модель прадукта"""
#     class Meta:
#         ordering = ["title", "price"]
#         verbose_name = "Product"
#         verbose_name_plural = "Products"
#
#     id = models.AutoField(primary_key=True)
#     category = models.PositiveIntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     count = models.PositiveIntegerField()
#     date = models.DateTimeField()
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     fullDescription = models.TextField()
#     freeDelivery = models.BooleanField(default=False)
#     rating = models.DecimalField(max_digits=3, blank=True, decimal_places=1, default=0.0)
#
#     # tags = models.ManyToManyField(Tag, related_name="products", verbose_name="Tags", blank=True)
#     # reviews = models.ForeignKey(Review, related_name="products", verbose_name="Reviews", blank=True, on_delete=models.CASCADE,)
#     # specifications = models.ManyToManyField(Specification, related_name="products", verbose_name="Specifications", blank=True)
#     # images = models.ManyToManyField(Image, related_name="products", verbose_name="Images", blank=True)
#

class Product(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="ID")
    category = models.PositiveIntegerField(verbose_name="Cathegory")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    count = models.PositiveIntegerField(verbose_name="Count")
    date = models.DateTimeField(verbose_name="Date")
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    fullDescription = models.TextField(blank=True, null=True, verbose_name="FullDescription")
    freeDelivery = models.BooleanField(default=False, verbose_name="FreeDelivery")
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Rating")


class Image(models.Model):
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    src = models.ImageField(
        upload_to="product_image/",
        default="default.png",
        verbose_name="Link",
        blank=True,
    )
    alt = models.CharField(max_length=128, blank=True, verbose_name="Description")
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    tag_id = models.AutoField(primary_key=True, verbose_name="Tag_ID")
    name = models.CharField(max_length=50, blank=True, verbose_name="Name")
    product = models.ForeignKey(Product, related_name='tags', on_delete=models.CASCADE)


class Review(models.Model):
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    author = models.CharField(max_length=255, verbose_name="Author")
    email = models.EmailField(unique=True, verbose_name="Email")
    text = models.TextField(verbose_name="Text")
    rate = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0, verbose_name="Rating")
    date = models.DateTimeField(verbose_name="Date")
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)


class Specification(models.Model):
    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    name = models.CharField(max_length=100, verbose_name="Name")
    value = models.CharField(max_length=255, verbose_name="Value")
    product = models.ForeignKey(Product, related_name='specifications', on_delete=models.CASCADE)



