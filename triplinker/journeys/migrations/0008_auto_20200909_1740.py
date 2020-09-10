# Generated by Django 3.0.8 on 2020-09-09 17:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journeys', '0007_auto_20200907_1721'),
    ]

    operations = [
        migrations.AddField(
            model_name='journey',
            name='visibility',
            field=models.CharField(choices=[('All', 'All users'), ('FriendsFollowers', 'Friends & followers'), ('Friends', 'Friends only'), ('Me', 'Only me')], max_length=16, null=True, verbose_name='The level of visibility'),
        ),
        migrations.AlterField(
            model_name='participant',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
