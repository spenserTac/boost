# Generated by Django 3.0.8 on 2020-10-10 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0062_acceptedcreatorordermodel_sponsor_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptedcreatorordermodel',
            name='sponsor_approves',
            field=models.BooleanField(default=False),
        ),
    ]