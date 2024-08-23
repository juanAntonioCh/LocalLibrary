# Generated by Django 4.2.7 on 2024-02-11 00:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_book_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='PDF',
            field=models.FileField(blank=True, null=True, upload_to='pdf_libros', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
