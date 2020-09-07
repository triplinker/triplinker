# Generated by Django 3.0.8 on 2020-09-02 17:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journeys', '0002_auto_20200902_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journey',
            name='who_added_the_journey',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='who_added', to=settings.AUTH_USER_MODEL, verbose_name="The person who has created the journey's page"),
        ),
    ]