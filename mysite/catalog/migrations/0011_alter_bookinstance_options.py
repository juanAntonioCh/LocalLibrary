# Generated by Django 4.2.7 on 2024-01-29 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_see_your_books', 'Can see your borrowed books'),)},
        ),
    ]