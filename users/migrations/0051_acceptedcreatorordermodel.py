# Generated by Django 3.0.8 on 2020-08-28 22:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0010_auto_20200816_2040'),
        ('sponsor_listings', '0007_auto_20200816_2040'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0050_auto_20200828_1354'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcceptedCreatorOrderModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buyer_listing', models.CharField(blank=True, max_length=500, null=True)),
                ('service', models.CharField(blank=True, max_length=500, null=True)),
                ('service_detailed', models.TextField(blank=True, max_length=1000, null=True)),
                ('status', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_username_accepted_creator_order', to=settings.AUTH_USER_MODEL)),
                ('buyers_listing_c', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyers_accepted_c_listing_for_c_order', to='creator_listings.BlogListingCreationModel')),
                ('buyers_listing_s', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyers_accepted_s_listing_for_c_order', to='sponsor_listings.SponsorListingCreationModel')),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_username_accepted_creator_listing', to=settings.AUTH_USER_MODEL)),
                ('creator_listing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accepted_creator_listing', to='creator_listings.BlogListingCreationModel')),
            ],
        ),
    ]