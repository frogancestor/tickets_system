# Generated by Django 5.0.4 on 2024-06-11 19:55

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0016_alter_autorizatedpeople_expiration_date_chat_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='autorizatedpeople',
            name='expiration_date',
            field=models.DateField(default=datetime.date(2024, 6, 16)),
        ),
        migrations.AlterField(
            model_name='chat',
            name='chat_name',
            field=models.CharField(default='298c3df5-f3de-4b20-8b15-2feb876149de', max_length=36, unique=True),
        ),
        migrations.AlterField(
            model_name='listattributedatareference',
            name='data',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='message',
            name='date_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
