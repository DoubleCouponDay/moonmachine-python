# Generated by Django 2.0.4 on 2018-07-27 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0010_auto_20180726_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelog',
            name='message',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='description',
            field=models.CharField(max_length=400),
        ),
    ]
