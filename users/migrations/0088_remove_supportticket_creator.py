# Generated by Django 3.0.8 on 2020-11-23 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0087_auto_20201123_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supportticket',
            name='creator',
        ),
    ]