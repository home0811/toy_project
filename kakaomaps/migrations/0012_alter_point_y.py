# Generated by Django 3.2.6 on 2021-08-31 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakaomaps', '0011_map_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='point',
            name='y',
            field=models.FloatField(null=True),
        ),
    ]
