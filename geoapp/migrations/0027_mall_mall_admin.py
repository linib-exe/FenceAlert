# Generated by Django 4.2.9 on 2024-03-08 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geoapp', '0026_alter_offer_detail_exp_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mall',
            name='mall_admin',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mall', to=settings.AUTH_USER_MODEL),
        ),
    ]
