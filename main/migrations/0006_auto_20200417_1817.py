# Generated by Django 2.2.6 on 2020-04-17 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20200417_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photos',
            name='tag',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='users',
            name='password',
            field=models.CharField(max_length=30),
        ),
    ]
