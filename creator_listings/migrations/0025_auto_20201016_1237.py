# Generated by Django 3.0.8 on 2020-10-16 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0024_remove_bloglistingcreationmodel_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='audience_description',
            field=models.CharField(blank=True, default=None, max_length=500000, null=True),
        ),
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='overview_description',
            field=models.CharField(blank=True, default=None, max_length=500000, null=True),
        ),
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='sponsor_description',
            field=models.CharField(blank=True, default=None, max_length=500000, null=True),
        ),
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='tagline',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]