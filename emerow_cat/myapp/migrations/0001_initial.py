# Generated by Django 5.0.1 on 2024-02-06 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Businesses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Company', models.CharField(db_column='Company', max_length=100)),
            ],
            options={
                'db_table': 'Businesses',
                'managed': False,
            },
        ),
    ]
