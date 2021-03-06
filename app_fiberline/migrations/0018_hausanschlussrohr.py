# Generated by Django 3.1.2 on 2020-10-25 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_fiberline', '0017_auto_20201024_1526'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hausanschlussrohr',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ort_kuerzel', models.CharField(blank=True, max_length=20, null=True)),
                ('strasse', models.CharField(max_length=50)),
                ('ha_number', models.IntegerField(default=0)),
                ('ha_add', models.CharField(blank=True, max_length=20, null=True)),
                ('we_number', models.IntegerField(default=1)),
                ('customer', models.CharField(blank=True, max_length=100, null=True)),
                ('project', models.CharField(blank=True, max_length=100, null=True)),
                ('cluster', models.CharField(blank=True, max_length=100, null=True)),
                ('technikstandort_id', models.CharField(blank=True, max_length=255, null=True)),
                ('technikstandort', models.CharField(blank=True, max_length=100, null=True)),
                ('einzelrohr_name', models.CharField(max_length=50)),
                ('einzelrohr_number', models.IntegerField(default=0)),
                ('fiberunit_size', models.CharField(choices=[('4er', '4er'), ('8er', '8er'), ('12er', '12er'), ('24er', '24er')], default='4er', max_length=10)),
                ('user_created', models.CharField(max_length=50)),
                ('user_updated', models.CharField(default='-', max_length=50)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('rohr_typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_fiberline.rohrtyp')),
            ],
            options={
                'ordering': ['customer', 'project', 'cluster', 'technikstandort', 'rohr_typ', 'einzelrohr_number'],
            },
        ),
    ]
