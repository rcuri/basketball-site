# Generated by Django 2.0.6 on 2019-01-16 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_auto_20181011_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='profile',
        ),
    ]