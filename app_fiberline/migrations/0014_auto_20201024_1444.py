# Generated by Django 3.1.2 on 2020-10-24 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0013_auto_20201024_1441'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Einzelrohr',
            new_name='RohrTyp',
        ),
    ]