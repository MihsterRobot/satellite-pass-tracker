'''Provides CRUD operations for models.'''

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .filters import PassFilter
from .models import Location, Satellite, Pass
from .serializers import LocationSerializer, SatelliteSerializer, PassSerializer
from .services import save_predicted_passes


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
    filterset_class = PassFilter

    @action(detail=False, methods=['post'], url_path='predict')
    def predict(self, request):
        satellite_id = request.data.get('satellite_id')
        location_id = request.data.get('location_id')

        if not satellite_id or not location_id:
            return Response({'error': 'satellite_id and location_id are required.'}, status=400)

        try:
            satellite = Satellite.objects.get(id=satellite_id)
            location = Location.objects.get(id=location_id)
        except (Satellite.DoesNotExist, Location.DoesNotExist):
            return Response({'error': 'Satellite or location not found.'}, status=404)

        passes = save_predicted_passes(satellite, location)
        serializer = self.get_serializer(passes, many=True)
        return Response(serializer.data, status=201)
