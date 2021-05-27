# Generated by Django 3.2.3 on 2021-05-25 14:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('request', '0003_auto_20210425_2233'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('execution_time', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('http_method', models.CharField(blank=True, max_length=255)),
                ('url', models.CharField(blank=True, max_length=255)),
                ('body', models.JSONField(blank=True, null=True)),
                ('headers', models.JSONField(blank=True, null=True)),
                ('params', models.JSONField(blank=True, null=True)),
                ('response', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]