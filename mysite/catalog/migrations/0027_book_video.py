# Generated by Django 4.2.7 on 2024-02-07 12:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_alter_book_portada'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='video',
            field=models.FileField(null=True, upload_to='videos_uploaded', validators=[django.core.validators.FileExtensionValidator(['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]
