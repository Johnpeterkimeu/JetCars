# Generated by Django 3.2.12 on 2023-01-13 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20230113_0700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Product_name',
            field=models.TextField(max_length=30),
        ),
    ]
