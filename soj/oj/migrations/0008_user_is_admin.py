# Generated by Django 3.1.5 on 2021-01-07 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oj', '0007_auto_20210107_1233'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]