# Generated by Django 3.0.8 on 2020-10-10 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0065_acceptedcreatorordermodel_edits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='acceptedcreatorordermodel',
            name='sponsor_change',
        ),
    ]
