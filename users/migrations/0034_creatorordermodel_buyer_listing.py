# Generated by Django 3.0.8 on 2020-08-23 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20200823_0222'),
    ]

    operations = [
        migrations.AddField(
            model_name='creatorordermodel',
            name='buyer_listing',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
