# Generated by Django 3.1.2 on 2020-10-28 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0027_auto_20201028_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hausanschlussrohr',
            name='ha_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='hausanschlussrohr',
            name='strasse',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hausanschlussrohr',
            name='we_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
