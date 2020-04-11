# Generated by Django 3.0.3 on 2020-04-10 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0051_auto_20200402_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.CharField(blank=True, max_length=200)),
                ('completed', models.BooleanField(default=False)),
                ('todo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='todo.ToDoItem')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
