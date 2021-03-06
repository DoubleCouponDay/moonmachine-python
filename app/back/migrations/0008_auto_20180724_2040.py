# Generated by Django 2.0.4 on 2018-07-24 08:40

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0007_auto_20180724_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='availablemarket',
            name='minimumprice',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AddField(
            model_name='availablemarket',
            name='minimumvolume',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
    ]
