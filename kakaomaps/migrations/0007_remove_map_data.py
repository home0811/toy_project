# Generated by Django 3.2.6 on 2021-08-26 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kakaomaps', '0006_auto_20210825_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='map',
            name='data',
        ),
    ]
