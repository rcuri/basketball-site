# Generated by Django 2.0.6 on 2018-10-15 01:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='game_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
