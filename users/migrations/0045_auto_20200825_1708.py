# Generated by Django 3.0.8 on 2020-08-25 21:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0010_auto_20200816_2040'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0044_auto_20200823_0322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creatorordermodel',
            name='buyer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_username', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creatorordermodel',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_username', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='creatorordermodel',
            name='creator_listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creator_listing', to='creator_listings.BlogListingCreationModel'),
        ),
    ]
