# Generated by Django 4.2.1 on 2023-05-23 15:49

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_item_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="description",
            new_name="descripción",
        ),
    ]
