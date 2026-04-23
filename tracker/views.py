'''Provides CRUD operations for models.'''

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from .models import Location, Satellite, Pass
from .serializers import LocationSerializer, SatelliteSerializer, PassSerializer


# All viewsets support filtering via URL parameters.
class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()  # Tells the viewset which database records to work with.
    serializer_class = LocationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']


class SatelliteViewSet(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = SatelliteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'norad_id', 'satellite_type']


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['satellite', 'location']
