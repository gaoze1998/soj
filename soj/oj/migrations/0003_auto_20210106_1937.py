# Generated by Django 3.1.5 on 2021-01-06 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0002_auto_20210106_1936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdetail',
            name='age',
            field=models.IntegerField(),
        ),
    ]
