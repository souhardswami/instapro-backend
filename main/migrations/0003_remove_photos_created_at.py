# Generated by Django 2.2.6 on 2020-04-17 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200417_1700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photos',
            name='created_at',
        ),
    ]
