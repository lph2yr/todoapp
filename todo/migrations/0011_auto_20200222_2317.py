# Generated by Django 3.0.3 on 2020-02-23 04:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0010_todoitem_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='duedate',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='todoitem',
            name='end_recur_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now),
        ),
        migrations.CreateModel(
            name='Recurrence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=600)),
                ('duedate', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('completed', models.BooleanField(default=False)),
                ('recur_freq', models.CharField(choices=[('NEVER', 'Never'), ('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], default='NEVER', max_length=7)),
                ('end_recur_date', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('priority', models.CharField(choices=[('HI', 'High'), ('MD', 'Medium'), ('LO', 'Low')], default='LO', max_length=2)),
                ('todo_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.ToDoItem')),
            ],
        ),
    ]
