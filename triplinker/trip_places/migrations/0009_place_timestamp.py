# Generated by Django 3.0.8 on 2020-09-06 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_places', '0008_auto_20200901_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
