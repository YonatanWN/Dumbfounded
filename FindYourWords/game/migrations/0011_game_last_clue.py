# Generated by Django 3.0.2 on 2020-05-28 16:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_player_connected'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='last_clue',
            field=models.DateTimeField(default=datetime.datetime(2000, 1, 1, 0, 0)),
        ),
    ]