# Generated by Django 2.0.4 on 2018-07-27 04:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0011_auto_20180727_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicelog',
            name='stacktrace',
            field=models.CharField(default=django.utils.timezone.now, max_length=100000),
            preserve_default=False,
        ),
    ]
