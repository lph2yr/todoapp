# Generated by Django 3.0.3 on 2020-03-21 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0050_auto_20200321_1732'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extracurricular',
            old_name='end_time',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='extracurricular',
            old_name='start_time',
            new_name='start_date',
        ),
    ]
