# Generated by Django 3.2.6 on 2021-08-26 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kakaomaps', '0007_remove_map_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='map',
            old_name='fill_color',
            new_name='fillColor',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='fill_opacity',
            new_name='fillOpacity',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='stroke_color',
            new_name='strokeColor',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='stroke_opacity',
            new_name='strokeOpacity',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='stroke_style',
            new_name='strokeStyle',
        ),
        migrations.RenameField(
            model_name='map',
            old_name='stroke_weight',
            new_name='strokeWeight',
        ),
    ]