# Generated by Django 2.1.5 on 2019-05-14 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_auto_20190514_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='splash',
            name='latest_version',
            field=models.URLField(default='', max_length=500, verbose_name='download link'),
        ),
    ]
