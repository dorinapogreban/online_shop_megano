# Generated by Django 4.1.6 on 2024-07-12 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orderapp", "0018_alter_order_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="PaymentSomeone",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.CharField(max_length=8, verbose_name="Card Number")),
                ("status", models.CharField(default="pending", max_length=20)),
                (
                    "error_message",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="orderapp.order"
                    ),
                ),
            ],
            options={
                "verbose_name": "Payment Someone",
                "verbose_name_plural": "Payments Someone",
            },
        ),
    ]
