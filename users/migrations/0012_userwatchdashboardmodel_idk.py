# Generated by Django 3.0.8 on 2020-08-19 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0010_auto_20200816_2040'),
        ('users', '0011_auto_20200818_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwatchdashboardmodel',
            name='idk',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='creator_listings.BlogListingCreationModel'),
        ),
    ]