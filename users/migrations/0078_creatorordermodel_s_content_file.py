# Generated by Django 3.0.8 on 2020-11-08 03:00

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0077_auto_20201106_1953'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorordermodel',
            name='s_content_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to=users.models.CreatorOrderModel.s_content_file_path),
        ),
    ]