# Generated by Django 4.1.6 on 2024-06-29 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderapp", "0009_rename_quantity_orderitem_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="city",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="City"
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="deliveryType",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ordinary", "Free Delivery"),
                    ("express", "Express Delivery"),
                ],
                default="ordinary",
                max_length=10,
                null=True,
                verbose_name="Delivery Type",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="paymentType",
            field=models.CharField(
                blank=True,
                choices=[("online", "Online Card"), ("someone", "Online Account")],
                default="online",
                max_length=10,
                null=True,
                verbose_name="Payment Type",
            ),
        ),
        migrations.AlterField(
            model_name="order",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("pending", "Pending"), ("accepted", "Accepted")],
                default="pending",
                max_length=10,
                null=True,
                verbose_name="Status",
            ),
        ),
    ]
