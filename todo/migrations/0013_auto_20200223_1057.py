# Generated by Django 3.0.3 on 2020-02-23 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0012_auto_20200222_2319'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurrence',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='description',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='end_recur_date',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='location',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='recur_freq',
        ),
        migrations.RemoveField(
            model_name='recurrence',
            name='title',
        ),
    ]
