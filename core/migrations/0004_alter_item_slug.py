# Generated by Django 4.2.1 on 2023-05-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_item_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="slug",
            field=models.SlugField(default="Producto_de_prueba"),
        ),
    ]
