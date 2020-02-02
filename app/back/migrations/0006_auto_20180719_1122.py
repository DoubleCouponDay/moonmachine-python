# Generated by Django 2.0.4 on 2018-07-18 23:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('back', '0005_independent_reserve_marketinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='extendeduser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenumber', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameModel(
            old_name='availablemarkets',
            new_name='availablemarket',
        ),
        migrations.RenameModel(
            old_name='regionalfarmers',
            new_name='regionalfarmer',
        ),
        migrations.RenameModel(
            old_name='servicelogs',
            new_name='servicelog',
        ),
    ]