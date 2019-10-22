# Generated by Django 2.2.6 on 2019-10-19 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exchange', '0006_delete_ticketoffering'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketOffering',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('username', models.CharField(max_length=200)),
                ('ttype', models.CharField(max_length=6)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exchange.Game')),
            ],
        ),
    ]
