# Generated by Django 3.0.3 on 2020-04-01 23:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('todo', '0049_auto_20200329_2328'),
    ]

    operations = [
        migrations.AddField(
            model_name='todoitem',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to=settings.AUTH_USER_MODEL),
        ),
    ]
