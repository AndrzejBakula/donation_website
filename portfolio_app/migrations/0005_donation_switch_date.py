# Generated by Django 3.1.3 on 2020-11-29 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0004_donation_is_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='switch_date',
            field=models.DateField(default=None, null=True),
        ),
    ]
