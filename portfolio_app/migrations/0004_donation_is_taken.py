# Generated by Django 3.1.3 on 2020-11-29 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_app', '0003_donation'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='is_taken',
            field=models.BooleanField(default=False),
        ),
    ]
