# Generated by Django 3.1.7 on 2021-02-24 19:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Imie')),
                ('last_name', models.CharField(blank=True, max_length=64, null=True, verbose_name='Last name')),
                ('email', models.EmailField(blank=True, max_length=64, null=True)),
                ('is_owner', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('client', models.ManyToManyField(to='accounts.Client')),
            ],
        ),
    ]
