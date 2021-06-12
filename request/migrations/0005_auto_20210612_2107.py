# Generated by Django 3.2.3 on 2021-06-12 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0006_auto_20210612_1848'),
        ('module', '0003_alter_module_table'),
        ('request', '0004_requesthistory'),
    ]

    operations = [
        migrations.AddField(
            model_name='requesthistory',
            name='module',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='module.module'),
        ),
        migrations.AddField(
            model_name='requesthistory',
            name='scenario_history',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='scenario.scenariohistory'),
        ),
        migrations.AddField(
            model_name='requesthistory',
            name='status',
            field=models.CharField(blank=True, default='pending', max_length=200),
        ),
        migrations.AddField(
            model_name='requesthistory',
            name='type',
            field=models.CharField(blank=True, default='single', max_length=200),
        ),
        migrations.AlterModelTable(
            name='requesthistory',
            table='request_histories',
        ),
    ]