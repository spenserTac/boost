# Generated by Django 3.0.8 on 2020-08-20 04:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sponsor_listings', '0007_auto_20200816_2040'),
        ('creator_listings', '0010_auto_20200816_2040'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0014_auto_20200819_2151'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creators_watched', models.ManyToManyField(blank=True, null=True, to='creator_listings.BlogListingCreationModel')),
                ('sponsors_watched', models.ManyToManyField(blank=True, null=True, to='sponsor_listings.SponsorListingCreationModel')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='UserWatchDashboardModel',
        ),
    ]
