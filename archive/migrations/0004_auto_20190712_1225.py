# Generated by Django 2.0.13 on 2019-07-12 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20190712_0918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='replay',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Replay'),
        ),
    ]
