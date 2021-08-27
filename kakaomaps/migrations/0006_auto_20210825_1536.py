# Generated by Django 3.2.6 on 2021-08-25 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kakaomaps', '0005_alter_map_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='map',
            name='coordinate',
            field=models.CharField(default='wgs84', max_length=100),
        ),
        migrations.AddField(
            model_name='map',
            name='fill_color',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='fill_opacity',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='stroke_color',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='stroke_opacity',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='stroke_style',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='stroke_weight',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='map',
            name='type',
            field=models.CharField(default='polyline', max_length=100),
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sequence', models.IntegerField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('map_id', models.ForeignKey(db_column='map_id', on_delete=django.db.models.deletion.CASCADE, related_name='map', to='kakaomaps.map')),
            ],
        ),
    ]
