# Generated by Django 3.2 on 2022-02-19 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentId', models.IntegerField(default=0)),
                ('email', models.EmailField(default=False, max_length=40)),
                ('isMarked', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('image', models.TextField(null=True)),
                ('content', models.TextField(max_length=3000, null=True)),
                ('nickname', models.CharField(default=False, max_length=24)),
                ('stock', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentId', models.IntegerField(default=0)),
                ('email', models.EmailField(default=False, max_length=40)),
                ('isLike', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentId', models.IntegerField(default=0)),
                ('nickname', models.CharField(default=False, max_length=24)),
                ('replycontent', models.TextField(max_length=1000)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
    ]