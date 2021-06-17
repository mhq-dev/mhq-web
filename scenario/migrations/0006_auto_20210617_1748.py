# Generated by Django 3.2.3 on 2021-06-17 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0005_auto_20210613_0631'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scenariohistory',
            old_name='start_request_time',
            new_name='start_execution_time',
        ),
        migrations.AddField(
            model_name='scenariohistory',
            name='status',
            field=models.CharField(blank=True, default='pending', max_length=200),
        ),
    ]
