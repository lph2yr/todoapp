# Generated by Django 3.0.3 on 2020-03-13 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0042_auto_20200313_0118'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todoitem',
            name='has_category_changed',
        ),
    ]