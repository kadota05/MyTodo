# Generated by Django 4.2.17 on 2025-02-02 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Habit', '0003_alter_habitlog_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='habit',
            name='created_at',
            field=models.DateField(verbose_name='作成日'),
        ),
    ]
