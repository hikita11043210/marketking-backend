# Generated by Django 5.0.1 on 2025-02-11 17:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_setting_ebay_access_token_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='setting',
            name='user',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='settings', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
