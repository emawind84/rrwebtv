# Generated by Django 2.0.13 on 2019-07-11 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_replay_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='replay',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]