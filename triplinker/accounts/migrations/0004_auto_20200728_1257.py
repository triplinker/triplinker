# Generated by Django 3.0.8 on 2020-07-28 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20200727_1532'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friendrequest',
            options={'verbose_name': 'Friend request', 'verbose_name_plural': 'Friend requests'},
        ),
        migrations.AlterModelOptions(
            name='tlaccount',
            options={'verbose_name': 'Account', 'verbose_name_plural': 'Accounts'},
        ),
    ]