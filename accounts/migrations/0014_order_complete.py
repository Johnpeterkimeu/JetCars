# Generated by Django 3.2.12 on 2023-01-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20230116_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='complete',
            field=models.BooleanField(null=True),
        ),
    ]
