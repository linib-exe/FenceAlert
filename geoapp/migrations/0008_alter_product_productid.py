# Generated by Django 4.2.8 on 2024-01-02 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geoapp', '0007_remove_product_id_alter_product_productid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productId',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True),
        ),
    ]
