# Generated by Django 3.1.2 on 2020-10-28 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0025_auto_20201027_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='technikstandortdefault',
            name='fiberunit_48',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]