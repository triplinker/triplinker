# Generated by Django 3.0.8 on 2020-09-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_auto_20200922_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupchatmessage',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
