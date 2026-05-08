'''Serializers handle the conversion between JSON and Python objects and validate incoming data.'''

from rest_framework import serializers
from .models import Location, Satellite, Pass


class LocationSerializer(serializers.ModelSerializer):
    # The Meta class is a configuration block inside a class that defines how 
    # that class should behave or be interpreted by the framework.
    class Meta:
        model = Location
        fields = '__all__'
    
    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError('The latitude must be between -90 and 90.')
        return value
    
    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError('The longitude must be between -180 and 180.')
        return value
    
    def validate_altitude(self, value):
        if value < -430 or value > 8849:
            raise serializers.ValidationError('The altitude must be between -430 and 8,849 meters.')


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = '__all__'

    def validate_norad_id(self, value):
        if Satellite.objects.filter(norad_id=value).exists():
            raise serializers.ValidationError('A satellite with this NORAD ID already exists.')
        return value


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = ['id', 'satellite', 'location', 'datetime', 'duration_seconds', 'max_elevation_deg', 'notes']

    def validate_max_elevation(self, value):
        if value < 0 or value > 90:
            raise serializers.ValidationError('The max elevation must be a number between 0 and 90.')
        return value
    
    # Override default output to nest full satellite and location objects instead of just their IDs.
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['satellite'] = SatelliteSerializer(instance.satellite).data
        representation['location'] = LocationSerializer(instance.location).data
        return representation
