# Generated by Django 2.0.4 on 2018-06-12 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('back', '0017_auto_20180612_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='language',
            field=models.ForeignKey(db_column='language_id', db_index=False, on_delete=django.db.models.deletion.CASCADE, to='back.language'),
        ),
        migrations.AlterField(
            model_name='usersstrategy',
            name='strategy',
            field=models.ForeignKey(db_column='strategy_id', db_index=False, on_delete=django.db.models.deletion.CASCADE, to='back.strategy'),
        ),
    ]
