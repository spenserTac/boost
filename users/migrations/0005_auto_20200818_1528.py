# Generated by Django 3.0.8 on 2020-08-18 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0010_auto_20200816_2040'),
        ('users', '0004_auto_20200817_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwatchdashboardmodel',
            name='watched_creator',
            field=models.ForeignKey(blank=True, db_column='f', default=None, on_delete=django.db.models.deletion.CASCADE, to='creator_listings.BlogListingCreationModel'),
        ),
    ]