# Generated by Django 4.2.9 on 2024-03-06 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0025_offer_detail_exp_count_offer_dismissed_count_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='detail_exp_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='dismissed_count',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='received_count',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
