# Generated by Django 4.2.17 on 2025-01-24 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PriorityTask', '0003_alter_prioritytask_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prioritytask',
            name='created_date',
            field=models.DateField(auto_now_add=True, verbose_name='作成日'),
        ),
    ]
