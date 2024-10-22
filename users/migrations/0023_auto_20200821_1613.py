# Generated by Django 3.0.8 on 2020-08-21 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor_listings', '0007_auto_20200816_2040'),
        ('creator_listings', '0010_auto_20200816_2040'),
        ('users', '0022_auto_20200821_1609'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='Profile',
            name='ordered_creators',
        ),
        migrations.RemoveField(
            model_name='Profile',
            name='ordered_sponsors',
        ),
        migrations.AddField(
            model_name='Profile',
            name='creators_u_ordered',
            field=models.ManyToManyField(blank=True, related_name='creators_u_ordered', to='creator_listings.BlogListingCreationModel'),
        ),
        migrations.AddField(
            model_name='Profile',
            name='creators_who_ordered_u',
            field=models.ManyToManyField(blank=True, related_name='creators_who_ordered_u', to='creator_listings.BlogListingCreationModel'),
        ),
        migrations.AddField(
            model_name='Profile',
            name='sponsors_u_ordered',
            field=models.ManyToManyField(blank=True, related_name='sponsors_u_ordered', to='sponsor_listings.SponsorListingCreationModel'),
        ),
        migrations.AddField(
            model_name='Profile',
            name='sponsors_who_ordered_u',
            field=models.ManyToManyField(blank=True, related_name='sponsors_who_ordered_u', to='creator_listings.BlogListingCreationModel'),
        ),
    ]
