# Generated by Django 3.0.8 on 2020-08-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserCreationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=300)),
                ('last_name', models.CharField(max_length=300)),
                ('email', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=300)),
            ],
        ),
    ]
