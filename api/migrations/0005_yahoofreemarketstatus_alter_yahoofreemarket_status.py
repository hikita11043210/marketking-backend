# Generated by Django 5.0.1 on 2025-02-26 15:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_yahoofreemarket_end_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='YahooFreeMarketStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'm_yahoo_free_market_status',
            },
        ),
        migrations.AlterField(
            model_name='yahoofreemarket',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.yahoofreemarketstatus'),
        ),
    ]
