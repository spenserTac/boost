# Generated by Django 3.0.8 on 2020-10-12 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0067_acceptedcreatorordermodel_review_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acceptedcreatorordermodel',
            name='review_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to='boost/users/review/'),
        ),
        migrations.AlterField(
            model_name='acceptedcreatorordermodel',
            name='turn',
            field=models.CharField(blank=True, default='c', max_length=10, null=True),
        ),
    ]