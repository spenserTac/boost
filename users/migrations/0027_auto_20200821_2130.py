# Generated by Django 3.0.8 on 2020-08-22 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_auto_20200821_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_creator_is_looking_for',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_sponsor_is_looking_for',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
