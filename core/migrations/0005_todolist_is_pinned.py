# Generated by Django 2.2 on 2021-02-23 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20210222_1949'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]