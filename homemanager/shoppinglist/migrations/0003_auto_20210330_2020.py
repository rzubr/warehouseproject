# Generated by Django 3.1.7 on 2021-03-30 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0002_auto_20210330_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppinglist',
            name='completed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]