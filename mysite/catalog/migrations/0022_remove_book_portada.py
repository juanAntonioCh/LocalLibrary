# Generated by Django 4.2.7 on 2024-02-01 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0021_book_portada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='portada',
        ),
    ]
