# Generated by Django 2.1.5 on 2019-03-28 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iotdevice', '0007_auto_20190329_0100'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicetype',
            name='latest_firmware',
            field=models.FileField(default='FW/icon.png', upload_to='FW/%Y/%m/%d', verbose_name='Firmware'),
        ),
    ]