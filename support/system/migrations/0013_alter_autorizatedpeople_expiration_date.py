# Generated by Django 5.0.4 on 2024-05-19 21:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_alter_credentials_login_autorizatedpeople'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizatedpeople',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2024, 5, 25)),
        ),
    ]
