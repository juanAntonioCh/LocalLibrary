# Generated by Django 4.2.7 on 2024-02-01 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0022_remove_book_portada'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='portada',
            field=models.ImageField(blank=True, null=True, upload_to='portadas'),
        ),
    ]
