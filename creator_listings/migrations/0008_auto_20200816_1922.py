# Generated by Django 3.0.8 on 2020-08-16 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0007_auto_20200815_2105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloglistingcreationmodel',
            old_name='blog_name',
            new_name='blog_url',
        ),
    ]