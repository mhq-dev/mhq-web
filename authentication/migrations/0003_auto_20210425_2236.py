# Generated by Django 3.1.7 on 2021-04-25 18:06

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20210409_1756'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=authentication.models.path_and_rename),
        ),
    ]
