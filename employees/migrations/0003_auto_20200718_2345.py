# Generated by Django 3.0.8 on 2020-07-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0002_auto_20200718_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employees',
            name='email',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='employees',
            name='jobnumber',
            field=models.CharField(max_length=32, unique=True),
        ),
    ]