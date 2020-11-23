# Generated by Django 3.0.2 on 2020-06-06 06:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_game_last_clue'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='timer_ended',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='last_clue',
            field=models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc)),
        ),
    ]