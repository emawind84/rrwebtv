# Generated by Django 2.0.13 on 2019-03-29 05:22

from django.db import migrations, models
import django.db.models.deletion
import uploads.core.models
import uploads.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20190329_0457'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replay', models.FileField(blank=True, null=True, upload_to=uploads.core.models.replay_directory_path, validators=[uploads.core.validators.validate_file_size, uploads.core.validators.validate_replay_file])),
            ],
        ),
        migrations.RenameField(
            model_name='document',
            old_name='replay',
            new_name='replays',
        ),
        migrations.AddField(
            model_name='replay',
            name='document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Document'),
        ),
    ]