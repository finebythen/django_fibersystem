# Generated by Django 3.1.2 on 2020-10-28 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0028_auto_20201028_1406'),
    ]

    operations = [
        migrations.AddField(
            model_name='hausanschlussrohr',
            name='ort',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
