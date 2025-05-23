# Generated by Django 5.0.1 on 2025-05-01 06:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_alter_expense_detail'),
    ]

    operations = [
        migrations.AddField(
            model_name='ebay',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ebay_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ebay',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ebay_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ebayskuhistory',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ebay_sku_history_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ebayskuhistory',
            name='update_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='ebayskuhistory',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='ebay_sku_history_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='expense',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='expense_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchase',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='purchase_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sales',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sales',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sales_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yahooauction',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='yahoo_auction_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yahooauction',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='yahoo_auction_update_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yahoofreemarket',
            name='insert_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='yahoo_free_market_insert_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='yahoofreemarket',
            name='update_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='yahoo_free_market_update_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
