# Generated by Django 3.0.8 on 2020-08-30 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip_places', '0006_auto_20200830_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.CharField(choices=[('no', 'Without any assessment'), ('1', '★'), ('2', '★★'), ('3', '★★★'), ('4', '★★★★'), ('5', '★★★★★')], max_length=25, verbose_name='The rating of place'),
        ),
    ]
