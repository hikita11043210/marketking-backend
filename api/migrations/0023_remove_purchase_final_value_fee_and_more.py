# Generated by Django 5.0.1 on 2025-04-28 02:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_purchase_ebay_id_sale_ebay_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='final_value_fee',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='import_tax',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='international_fee',
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.DeleteModel(
            name='Sale',
        ),
        migrations.CreateModel(
            name='Sales',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField()),
                ('product_name', models.TextField(null=True)),
                ('management_code', models.CharField(blank=True, max_length=100, null=True)),
                ('url', models.TextField(blank=True, null=True)),
                ('identification_type', models.CharField(blank=True, max_length=50, null=True)),
                ('identification_number', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('import_tax', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('final_value_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('international_fee', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('tax', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('shipping_cost', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('client_name', models.CharField(blank=True, max_length=100, null=True)),
                ('client_company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('client_postal_code', models.CharField(blank=True, max_length=100, null=True)),
                ('client_address', models.TextField(blank=True, null=True)),
                ('client_occupation', models.CharField(blank=True, max_length=100, null=True)),
                ('client_age', models.IntegerField(blank=True, null=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('update_datetime', models.DateTimeField(auto_now=True)),
                ('insert_datetime', models.DateTimeField(auto_now_add=True)),
                ('ebay_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ebay')),
            ],
            options={
                'db_table': 't_sales',
            },
        ),
    ]
