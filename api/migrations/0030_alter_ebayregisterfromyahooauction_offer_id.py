# Generated by Django 5.0.1 on 2025-02-20 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_ebayregisterfromyahooauction_offer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebayregisterfromyahooauction',
            name='offer_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
