# Generated by Django 3.1.7 on 2021-04-12 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('request', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]