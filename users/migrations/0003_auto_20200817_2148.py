# Generated by Django 3.0.8 on 2020-08-18 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0010_auto_20200816_2040'),
        ('sponsor_listings', '0007_auto_20200816_2040'),
        ('users', '0002_auto_20200817_1727'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwatchdashboardmodel',
            name='user',
            field=models.CharField(default=None, max_length=300),
        ),
        migrations.AlterField(
            model_name='userwatchdashboardmodel',
            name='watched_creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='creator_listings.BlogListingCreationModel'),
        ),
        migrations.AlterField(
            model_name='userwatchdashboardmodel',
            name='watched_sponsor',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='sponsor_listings.SponsorListingCreationModel'),
        ),
    ]