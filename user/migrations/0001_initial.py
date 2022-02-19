# Generated by Django 3.2 on 2022-02-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nickname', models.CharField(max_length=24, unique=True)),
                ('email', models.EmailField(max_length=40, unique=True)),
            ],
            options={
                'db_table': 'User',
            },
        ),
    ]
