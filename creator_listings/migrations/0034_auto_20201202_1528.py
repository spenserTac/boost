# Generated by Django 3.0.8 on 2020-12-02 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator_listings', '0033_bloglistingcreationmodel_domain_authority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglistingcreationmodel',
            name='monthly_views',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]