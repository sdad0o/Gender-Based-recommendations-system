# Generated by Django 5.0.2 on 2024-02-18 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_delete_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_url',
            field=models.URLField(blank=True),
        ),
    ]