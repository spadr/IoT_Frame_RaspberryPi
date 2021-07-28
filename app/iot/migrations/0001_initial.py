# Generated by Django 3.1.6 on 2021-07-27 01:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import iot.views.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LD_status', models.BooleanField()),
                ('mail_status', models.BooleanField()),
                ('line_token', models.CharField(max_length=100)),
                ('line_token_status', models.BooleanField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NumberModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('data', models.FloatField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100)),
                ('time', models.DateTimeField()),
                ('filename', models.CharField(max_length=100, verbose_name='File Name')),
                ('image', models.ImageField(upload_to=iot.views.models.get_photo_upload_path, verbose_name='Photo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('channel', models.CharField(max_length=100)),
                ('data_type', models.CharField(max_length=100)),
                ('LD_status', models.BooleanField()),
                ('LD_min', models.IntegerField(null=True)),
                ('latest', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
