# Generated by Django 5.0.2 on 2024-02-18 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rating'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rating',
        ),
    ]