# Generated by Django 2.2.6 on 2019-10-19 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0009_ticketoffering'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketoffering',
            name='location',
            field=models.CharField(choices=[('HILL', 'Hill'), ('UPPER', 'Upper Deck'), ('LOWER', 'Lower Deck')], max_length=6),
        ),
    ]
