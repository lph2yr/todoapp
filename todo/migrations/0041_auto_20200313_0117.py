# Generated by Django 3.0.3 on 2020-03-13 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0040_todoitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cat',
            field=models.CharField(max_length=10, verbose_name='Category Name'),
        ),
        migrations.AlterField(
            model_name='specific',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.Category'),
        ),
    ]
