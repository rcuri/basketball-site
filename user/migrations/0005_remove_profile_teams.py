# Generated by Django 2.0.6 on 2019-01-17 05:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190116_1405'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='teams',
        ),
    ]