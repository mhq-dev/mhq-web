# Generated by Django 3.1.7 on 2021-04-25 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0002_auto_20210412_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='name',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='type',
            field=models.CharField(blank=True, default='public', max_length=255),
        ),
    ]
