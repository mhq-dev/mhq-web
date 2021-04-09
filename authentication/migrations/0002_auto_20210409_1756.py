# Generated by Django 3.1.7 on 2021-04-09 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='pictures/avatar/'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
