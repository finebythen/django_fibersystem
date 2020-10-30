from .models import Technikstandort, Hausanschlussrohr
import django_filters


class TstFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Technikstandort
        fields = ['name', 'cluster']


class HausanschlussrohrFilter(django_filters.FilterSet):
    ort = django_filters.CharFilter(field_name='ort', lookup_expr='contains')
    strasse = django_filters.CharFilter(field_name='strasse', lookup_expr='contains')

    class Meta:
        model = Hausanschlussrohr
        fields = ['ort', 'strasse', 'ha_number', 'ha_add']
