'''Defines custom filter sets for querying model data via URL parameters.'''

import django_filters

from .models import Pass


class PassFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name='datetime', lookup_expr='gte')
    end_date = django_filters.DateTimeFilter(field_name='datetime', lookup_expr='lte')

    class Meta:
        model = Pass
        fields = ['satellite', 'location', 'start_date', 'end_date']
