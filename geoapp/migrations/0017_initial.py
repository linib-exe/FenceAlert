# Generated by Django 4.1 on 2024-01-04 07:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('geoapp', '0016_delete_mallowner_remove_product_productowner_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopName', models.CharField(max_length=50)),
                ('shopOwner', models.CharField(default='Blank', max_length=50)),
                ('shopContact', models.CharField(default='9999999999', max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('productPrice', models.FloatField()),
                ('productCategory', models.CharField(choices=[('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Drinks', 'Drinks'), ('Furniture', 'Furniture')], default='Electronics', max_length=20)),
                ('productOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoapp.shop')),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offerprice', models.FloatField()),
                ('offeredby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoapp.shop')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geoapp.product')),
            ],
        ),
    ]
