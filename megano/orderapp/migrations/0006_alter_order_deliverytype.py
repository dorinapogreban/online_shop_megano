# Generated by Django 4.1.6 on 2024-06-18 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orderapp", "0005_alter_order_options_alter_orderitem_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="deliveryType",
            field=models.CharField(
                choices=[("free", "Free Delivery"), ("express", "Express Delivery")],
                default="free",
                max_length=10,
                verbose_name="Delivery Type",
            ),
        ),
    ]
