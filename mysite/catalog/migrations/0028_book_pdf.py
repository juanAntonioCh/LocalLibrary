# Generated by Django 4.2.7 on 2024-02-07 12:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_book_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='PDF',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['pdf'])]),
        ),
    ]
