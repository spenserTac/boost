# Generated by Django 3.0.8 on 2020-09-12 22:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0015_auto_20200912_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='monthly_views',
            field=models.CharField(blank=True, default=None, max_length=300, null=True),
        ),
    ]