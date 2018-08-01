# Generated by Django 2.0.4 on 2018-07-30 22:48

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0012_servicelog_stacktrace'),
    ]

    operations = [
        migrations.CreateModel(
            name='vaultoro_markethistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hoardedcurrency', models.CharField(max_length=40)),
                ('pricecurrency', models.CharField(max_length=40)),
                ('open', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('close', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('high', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('low', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('volume', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('miscellaneous', models.CharField(max_length=100000)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
