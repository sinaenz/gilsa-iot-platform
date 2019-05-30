# Generated by Django 2.1.5 on 2019-05-26 11:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_auto_20190523_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='splash',
            name='min_version',
        ),
        migrations.AddField(
            model_name='splash',
            name='minimum_version',
            field=models.IntegerField(blank=True, default=0, verbose_name='minimum version number'),
        ),
        migrations.AlterField(
            model_name='splash',
            name='latest_version',
            field=models.IntegerField(blank=True, default=0, verbose_name='latest version number'),
        ),
    ]