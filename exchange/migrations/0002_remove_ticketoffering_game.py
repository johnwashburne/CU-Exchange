# Generated by Django 2.2.6 on 2019-10-19 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketoffering',
            name='game',
        ),
    ]
