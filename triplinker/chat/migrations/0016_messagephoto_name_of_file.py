# Generated by Django 3.0.8 on 2020-09-25 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0015_messagephoto'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagephoto',
            name='name_of_file',
            field=models.TextField(blank=True, null=True, verbose_name='The name image'),
        ),
    ]