# Generated by Django 3.2.11 on 2022-05-18 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_firmwarefile_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='firmwarefile',
            name='state',
            field=models.BooleanField(default=False),
        ),
    ]
