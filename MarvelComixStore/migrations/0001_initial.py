# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comix',
            fields=[
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('description', models.TextField(verbose_name='Описание')),
                ('date', models.DateField(db_index=True, default=django.utils.timezone.now, verbose_name='Дата выхода')),
                ('ean', models.CharField(unique=True, serialize=False, primary_key=True, verbose_name='EAN', max_length=13)),
                ('cover', models.ImageField(upload_to='', verbose_name='Обложка')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('comixlist', models.ManyToManyField(to='MarvelComixStore.Comix')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='Тег')),
            ],
        ),
        migrations.AddField(
            model_name='comix',
            name='tags',
            field=models.ManyToManyField(to='MarvelComixStore.Tag', verbose_name='Теги'),
        ),
    ]
