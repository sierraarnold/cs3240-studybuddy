# Generated by Django 3.0.2 on 2020-04-12 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20200410_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(default='Inactive', max_length=50),
        ),
    ]
