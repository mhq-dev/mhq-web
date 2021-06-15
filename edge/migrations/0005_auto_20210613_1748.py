# Generated by Django 3.2.3 on 2021-06-13 13:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('module', '0003_auto_20210613_0536'),
        ('edge', '0004_alter_statement_edge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statement',
            name='name',
        ),
        migrations.AlterField(
            model_name='edge',
            name='dist',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='dist', to='module.module'),
        ),
        migrations.AlterField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='source', to='module.module'),
        ),
    ]