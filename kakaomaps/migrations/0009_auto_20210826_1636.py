# Generated by Django 3.2.6 on 2021-08-26 07:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kakaomaps', '0008_auto_20210826_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='map',
            name='fillOpacity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='strokeOpacity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='map',
            name='strokeWeight',
            field=models.FloatField(null=True),
        ),
    ]
