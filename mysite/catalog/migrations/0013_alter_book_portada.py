# Generated by Django 4.2.7 on 2024-02-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_book_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='portada',
            field=models.ImageField(null=True, upload_to='catalog/static/images/'),
        ),
    ]
