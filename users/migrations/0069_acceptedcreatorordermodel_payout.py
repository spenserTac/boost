# Generated by Django 3.0.8 on 2020-10-13 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0068_auto_20201011_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='acceptedcreatorordermodel',
            name='payout',
            field=models.IntegerField(blank=True, default=None, max_length=10000, null=True),
        ),
    ]