# Generated by Django 4.1.6 on 2024-05-15 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shopapp", "0018_alter_product_rating_alter_product_sales_count_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="specification",
            name="product",
        ),
        migrations.AddField(
            model_name="specification",
            name="product",
            field=models.ManyToManyField(
                blank=True, related_name="specifications", to="shopapp.product"
            ),
        ),
    ]
