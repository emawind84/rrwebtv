# Generated by Django 2.0.13 on 2019-03-29 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20190329_0522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='replays',
        ),
    ]
