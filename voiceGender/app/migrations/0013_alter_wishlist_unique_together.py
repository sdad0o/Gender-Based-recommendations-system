# Generated by Django 5.0.2 on 2024-02-23 19:24

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_wishlist'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='wishlist',
            unique_together={('user', 'product')},
        ),
    ]