# Generated by Django 2.0.9 on 2019-03-22 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20190322_0251'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='gdpr_accept',
            field=models.BooleanField(default=False),
        ),
    ]
