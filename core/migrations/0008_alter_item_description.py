# Generated by Django 4.2.1 on 2023-05-23 16:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0007_rename_descripción_item_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="description",
            field=models.TextField(default="Descripción de prueba"),
        ),
    ]
