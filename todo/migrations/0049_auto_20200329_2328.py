# Generated by Django 3.0.3 on 2020-03-30 03:28

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0048_merge_20200329_2231'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='notify',
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='duedate',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_recur_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
