# Generated by Django 2.0.4 on 2018-07-17 07:46

from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='availablemarkets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exchangename', models.CharField(max_length=40)),
                ('marketcode', models.CharField(max_length=40)),
                ('hoursavailable', models.BooleanField(default=False)),
                ('daysavailable', models.BooleanField(default=False)),
                ('monthsavailable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='independent_reserve_marketinfo',
            fields=[
                ('marketinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='back.marketinfo')),
            ],
            bases=('back.marketinfo',),
        ),
        migrations.CreateModel(
            name='regionalfarmers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hook', models.CharField(max_length=100000)),
                ('key', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='servicelogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logsdatetime', models.DateTimeField()),
                ('logslevel', models.CharField(max_length=40)),
                ('message', models.CharField(max_length=40)),
            ],
        ),
        migrations.AddField(
            model_name='marketinfo',
            name='close',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AddField(
            model_name='marketinfo',
            name='high',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AddField(
            model_name='marketinfo',
            name='open',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AddField(
            model_name='marketinfo',
            name='volume',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='given_amount',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='received_amount',
            field=models.DecimalField(decimal_places=18, default=Decimal('0'), max_digits=36),
        ),
    ]
