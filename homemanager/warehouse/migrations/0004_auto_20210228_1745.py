# Generated by Django 3.1.1 on 2021-02-28 16:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_auto_20210228_1734'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='stock_state',
            new_name='stock',
        ),
    ]
