'''Provides CRUD operations for models.'''

from rest_framework import viewsets
from .models import Location, Satellite, Pass
from .serializers import LocationSerializer, SatelliteSerializer, PassSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()  # Tells the viewset which database records to work with.
    serializer_class = LocationSerializer


class SatelliteViewSet(viewsets.ModelViewSet):
    queryset = Satellite.objects.all()
    serializer_class = SatelliteSerializer


class PassViewSet(viewsets.ModelViewSet):
    queryset = Pass.objects.all()
    serializer_class = PassSerializer
