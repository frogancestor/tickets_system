# Generated by Django 5.0.4 on 2024-05-11 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_remove_atrdatatypes_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customcategoryattributes',
            name='dataType',
        ),
    ]
