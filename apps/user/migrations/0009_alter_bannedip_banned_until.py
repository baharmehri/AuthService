# Generated by Django 4.2.14 on 2024-08-09 10:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_alter_bannedip_banned_until'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannedip',
            name='banned_until',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 9, 11, 45, 42, 502199, tzinfo=datetime.timezone.utc)),
        ),
    ]