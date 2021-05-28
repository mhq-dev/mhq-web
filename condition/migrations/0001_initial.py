# Generated by Django 3.2.3 on 2021-05-28 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('edge', '0003_alter_statement_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('operator', models.CharField(default='equal', max_length=250)),
                ('first', models.CharField(max_length=250)),
                ('second', models.CharField(max_length=250)),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='edge.statement')),
            ],
            options={
                'db_table': 'conditions',
            },
        ),
    ]