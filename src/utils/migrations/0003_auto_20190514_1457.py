# Generated by Django 2.1.5 on 2019-05-14 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_andriodupdate_iosupdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='andriodupdate',
            name='title',
            field=models.CharField(default='Andriod', max_length=200, verbose_name='Config Name'),
        ),
        migrations.AlterField(
            model_name='iosupdate',
            name='title',
            field=models.CharField(default='IOS', max_length=200, verbose_name='Config Name'),
        ),
    ]
