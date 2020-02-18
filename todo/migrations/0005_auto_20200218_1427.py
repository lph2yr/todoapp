# Generated by Django 3.0.3 on 2020-02-18 19:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0004_todoitem_priority'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='end_recur_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='todoitem',
            name='recur_freq',
            field=models.TextField(default=django.utils.timezone.now, max_length=7),
            preserve_default=False,
        ),
    ]
