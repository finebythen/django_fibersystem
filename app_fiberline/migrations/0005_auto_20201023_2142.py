# Generated by Django 3.1.2 on 2020-10-23 19:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0004_auto_20201023_2136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='schacht_kvz',
            old_name='kabel_versorgt',
            new_name='kabel_a_seite',
        ),
    ]