'''Serializers handle the conversion between JSON and Python objects and validate incoming data.'''

from rest_framework import serializers
from .models import Location, Satellite, Pass


class LocationSerializer(serializers.ModelSerializer):
    # The Meta class is a configuration block inside a class that defines how 
    # that class should behave or be interpreted by the framework.
    class Meta:
        model = Location
        fields = '__all__'


class SatelliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satellite
        fields = '__all__'


class PassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pass
        fields = '__all__'
