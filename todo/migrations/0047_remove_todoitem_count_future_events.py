# Generated by Django 3.0.3 on 2020-03-25 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0046_todoitem_future_events'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='count_future_events',
        ),
    ]