# Generated by Django 2.1.5 on 2019-01-31 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdevice', '0002_auto_20190131_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_connected',
            field=models.BooleanField(default=False, verbose_name='Is Connected?'),
        ),
    ]
