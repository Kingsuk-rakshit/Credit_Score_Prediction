# Generated by Django 4.2.7 on 2024-11-07 21:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditscoreprediction',
            name='amount_invested_monthly',
        ),
        migrations.RemoveField(
            model_name='creditscoreprediction',
            name='interest_rate',
        ),
        migrations.RemoveField(
            model_name='creditscoreprediction',
            name='total_emi_per_month',
        ),
    ]