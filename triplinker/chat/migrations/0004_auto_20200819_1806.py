# Generated by Django 3.0.8 on 2020-08-19 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_auto_20200819_1645'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='users_who_read_messages',
            new_name='users_who_read_message',
        ),
    ]
