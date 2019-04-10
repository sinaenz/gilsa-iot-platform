# Generated by Django 2.1.5 on 2019-01-31 13:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Device Name')),
                ('device_id', models.UUIDField(default=uuid.uuid4, verbose_name='Device ID')),
            ],
        ),
    ]