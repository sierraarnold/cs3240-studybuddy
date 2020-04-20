# Generated by Django 3.0.2 on 2020-04-16 19:39

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20200412_2326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='inappmessage',
            name='title',
        ),
        migrations.AddField(
            model_name='inappmessage',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
