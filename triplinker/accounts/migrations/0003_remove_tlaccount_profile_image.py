# Generated by Django 3.0.8 on 2020-10-04 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_tlaccount_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tlaccount',
            name='profile_image',
        ),
    ]
