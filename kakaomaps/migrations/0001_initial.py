# Generated by Django 3.2.6 on 2021-08-24 07:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matrix',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('data', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=8), size=8)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
