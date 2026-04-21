'''Serializers help validate incoming data and handle the conversion of JSON to Python objects.'''

from rest_framework import serializers
from .models import Location, Satellite, Pass

'''
When a request comes in with JSON data, or when your API needs to send data back as JSON, 
something needs to handle the conversion between JSON and Python objects — and also 
validate incoming data. That's what a serializer does. For each model, you'll have a corresponding 
serializer. DRF's ModelSerializer makes this straightforward — you just 
tell it which model it's for and which fields to include.
'''


class LocationSerializer(serializers.ModelSerializer):
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
