# Generated by Django 3.1.5 on 2021-01-08 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0009_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='sample_location',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
    ]