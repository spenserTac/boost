# Generated by Django 3.0.8 on 2020-08-19 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200818_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userwatchdashboardmodel',
            name='user',
            field=models.TextField(null=True),
        ),
    ]
