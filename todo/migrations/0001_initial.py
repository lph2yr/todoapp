# Generated by Django 3.0.3 on 2020-02-11 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ToDoItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=50)),
                ('completed', models.BooleanField(default=False)),
            ],
        ),
    ]
