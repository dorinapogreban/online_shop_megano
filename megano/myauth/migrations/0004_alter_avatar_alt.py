# Generated by Django 4.1.6 on 2024-04-15 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myauth", "0003_alter_avatar_alt"),
    ]

    operations = [
        migrations.AlterField(
            model_name="avatar",
            name="alt",
            field=models.CharField(
                blank=True, max_length=128, null=True, verbose_name="Description"
            ),
        ),
    ]
