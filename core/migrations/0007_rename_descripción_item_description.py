# Generated by Django 4.2.1 on 2023-05-23 15:50

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0006_rename_description_item_descripción"),
    ]

    operations = [
        migrations.RenameField(
            model_name="item",
            old_name="descripción",
            new_name="description",
        ),
    ]
