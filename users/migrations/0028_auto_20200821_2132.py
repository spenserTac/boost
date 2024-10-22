# Generated by Django 3.0.8 on 2020-08-22 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor_listings', '0007_auto_20200816_2040'),
        ('creator_listings', '0010_auto_20200816_2040'),
        ('users', '0027_auto_20200821_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creator_order',
            name='buyers_listing_for_creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyers_creator_listing', to='creator_listings.BlogListingCreationModel'),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='buyers_listing_for_sponsor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sponsor_listings.SponsorListingCreationModel'),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_creator_is_looking_for',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_creator_is_looking_fordetailed',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_sponsor_is_looking_for',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='creator_order',
            name='what_services_sponsor_is_looking_for_detailed',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
    ]
