# Generated by Django 3.2.12 on 2023-01-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_product_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Product_name',
            field=models.CharField(max_length=30),
        ),
    ]
