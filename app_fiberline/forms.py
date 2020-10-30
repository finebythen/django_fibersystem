from django.forms import ModelForm
from .models import *


class Create_Schacht_Kvz_Form(ModelForm):
    class Meta:
        model = Schacht_Kvz
        exclude = [
            'customer',
            'project',
            'cluster',
            'technikstandort_id',
            'technikstandort',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Create_Kabel_Form(ModelForm):
    class Meta:
        model = Kabel
        exclude = [
            'faser_anzahl',
            'user_created',
            'date_created',
        ]


class Create_Rohr_Form(ModelForm):
    class Meta:
        model = Rohr
        exclude = [
            'customer',
            'project',
            'cluster',
            'technikstandort_id',
            'technikstandort',
            'schacht_kvz',
            'user_created',
            'date_created',
        ]


class Create_Technikstandort_Default_Form(ModelForm):
    class Meta:
        model = TechnikstandortDefault
        exclude = [
            'customer',
            'project',
            'cluster',
            'technikstandort_name',
            'technikstandort_id',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Create_Einzelrohr_Form(ModelForm):
    class Meta:
        model = Hausanschlussrohr
        exclude = [
            'we_number',
            'customer',
            'project',
            'cluster',
            'technikstandort_id',
            'technikstandort',
            'schacht_kvz',
            'rohr_typ',
            'rohr_name',
            'einzelrohr_name',
            'fiberunit_size',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Create_Wohneinheit_Form(ModelForm):
    class Meta:
        model = Wohneinheit
        exclude = [
            'hausanschlussrohr',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Combine_Schacht_Kvz_Kabel_Form(ModelForm):
    class Meta:
        model = Schacht_Kvz
        exclude = [
            'name',
            'customer',
            'project',
            'cluster',
            'technikstandort_id',
            'technikstandort',
            'type',
            'rohr_abgaenge',
            'rohr_einzelrohre_typ',
            'kabel_status_versorgt',
            'geo_latitude',
            'geo_longitude',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Update_Schacht_Kvz_Form(ModelForm):
    class Meta:
        model = Schacht_Kvz
        exclude = [
            'name',
            'customer',
            'project',
            'cluster',
            'technikstandort_id',
            'technikstandort',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]


class Update_Kabel_Form(ModelForm):
    class Meta:
        model = Kabel
        exclude = [
            'name',
            'faser_anzahl',
            'user_created',
            'date_created',
        ]


class Update_Technikstandort_Default_Form(ModelForm):
    class Meta:
        model = TechnikstandortDefault
        exclude = [
            'customer',
            'project',
            'cluster',
            'technikstandort_name',
            'technikstandort_id',
            'user_created',
            'user_updated',
            'date_created',
            'date_updated',
        ]
