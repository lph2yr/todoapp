# Generated by Django 3.0.3 on 2020-02-18 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_auto_20200217_1914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='end_recur_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
