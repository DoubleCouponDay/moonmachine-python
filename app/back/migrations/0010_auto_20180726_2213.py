# Generated by Django 2.0.4 on 2018-07-26 10:13

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0009_auto_20180725_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='availableexchange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchangename', models.CharField(max_length=40)),
                ('hoursavailable', models.BooleanField(default=False)),
                ('daysavailable', models.BooleanField(default=False)),
                ('weeksavailable', models.BooleanField(default=False)),
                ('monthsavailable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='independent_reserve_markethistory',
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
        migrations.CreateModel(
            name='marketticker',
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
                ('timestamp', models.DateTimeField()),
                ('currenthighestbid', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('currentlowestprice', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
                ('daysaverageprice', models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='independent_reserve_marketdata',
        ),
        migrations.RemoveField(
            model_name='availablemarket',
            name='daysavailable',
        ),
        migrations.RemoveField(
            model_name='availablemarket',
            name='exchangename',
        ),
        migrations.RemoveField(
            model_name='availablemarket',
            name='hoursavailable',
        ),
        migrations.RemoveField(
            model_name='availablemarket',
            name='marketcode',
        ),
        migrations.RemoveField(
            model_name='availablemarket',
            name='monthsavailable',
        ),
        migrations.AddField(
            model_name='availablemarket',
            name='hoardedcurrency',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availablemarket',
            name='pricecurrency',
            field=models.CharField(default=0, max_length=40),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availablemarket',
            name='currentticker',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to='back.marketticker'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='availablemarket',
            name='exchange',
            field=models.ForeignKey(db_column='exchange_id', db_index=False, default='', on_delete=django.db.models.deletion.CASCADE, to='back.availableexchange'),
            preserve_default=False,
        ),
    ]
