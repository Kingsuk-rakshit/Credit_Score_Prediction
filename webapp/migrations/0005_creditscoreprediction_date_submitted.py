# Generated by Django 4.2.7 on 2024-11-07 23:18

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_creditscoreprediction_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditscoreprediction',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]