# Generated by Django 3.1.2 on 2020-10-27 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0024_hausanschlussrohr_einzelrohr_malfunction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hausanschlussrohr',
            options={'ordering': ['customer', 'project', 'cluster', 'technikstandort', 'schacht_kvz', 'rohr_typ']},
        ),
        migrations.RemoveField(
            model_name='hausanschlussrohr',
            name='einzelrohr_number',
        ),
    ]
