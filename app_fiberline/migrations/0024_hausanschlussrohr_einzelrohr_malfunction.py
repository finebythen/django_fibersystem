# Generated by Django 3.1.2 on 2020-10-27 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0023_hausanschlussrohr_rohr_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hausanschlussrohr',
            name='einzelrohr_malfunction',
            field=models.BooleanField(default=False),
        ),
    ]
