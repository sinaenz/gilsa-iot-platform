# Generated by Django 2.1.5 on 2019-03-26 22:12

from django.db import migrations, models
import iotauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('phone', models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='phone')),
                ('full_name', models.CharField(blank=True, max_length=40, null=True, unique=True, verbose_name='full name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('avatar', models.ImageField(default='avatar/avatar.png', upload_to='avatar/%Y/%m/%d', verbose_name='Avatar')),
                ('verification_code', models.CharField(blank=True, max_length=120, null=True, verbose_name='Verification Code')),
                ('is_verified', models.BooleanField(default=False, verbose_name='is verified?')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', iotauth.models.UserManager()),
            ],
        ),
    ]
