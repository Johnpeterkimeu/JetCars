# Generated by Django 3.2.12 on 2023-01-10 12:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Image',
        ),
    ]