# Generated by Django 4.2.1 on 2023-06-02 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0013_billingaddress"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="billing_adress",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="core.billingaddress",
            ),
        ),
    ]
