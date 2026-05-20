'''Unit tests for tracker serializers.'''

import datetime

from django.test import TestCase

from tracker.models import Location, Satellite
from tracker.serializers import LocationSerializer, SatelliteSerializer, PassSerializer


class LocationSerializerTest(TestCase):
    def test_valid_coordinates_are_accepted(self):
        data = {
            'name': 'Test Location',
            'latitude': 45.0,
            'longitude': 90.0,
            'altitude_m': 100.0
        }
        serializer = LocationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_latitude_value_outside_90_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': 100.0,
            'longitude': 0.0,
            'altitude_m': 0.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_latitude_value_outside_negative_90_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': -100.0,
            'longitude': 0.0,
            'altitude_m': 0.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_longitude_value_outside_180_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': 0.0,
            'longitude': 200.0,
            'altitude_m': 0.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_longitude_value_outside_negative_180_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': 0.0,
            'longitude': -200.0,
            'altitude_m': 0.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_altitude_value_outside_8849_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': 0.0,
            'longitude': 0.0,
            'altitude_m': 9000.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_altitude_value_outside_negative_430_is_rejected(self):
        data = {
            'name': 'Test Location',
            'latitude': 0.0,
            'longitude': 0.0,
            'altitude_m': -500.0
        }
        serializer = LocationSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class SatelliteSerializerTest(TestCase):
    def test_duplicate_norad_id_is_rejected(self):
        data1 = {
            'name': 'PACE',
            'norad_id': 12345,
            'satellite_type': 'Observation',
            'description': 'Engineered to explore the Universe.'
        }
        data2 = {
            'name': 'JWST',
            'norad_id': 12345,
            'satellite_type': 'Observation',
            'description': 'Engineered to explore Mars.'
        }
        serializer1 = SatelliteSerializer(data=data1)
        self.assertTrue(serializer1.is_valid())
        serializer1.save()
        serializer2 = SatelliteSerializer(data=data2)
        self.assertFalse(serializer2.is_valid())
        

class PassSerializerTest(TestCase):
    def setUp(self):
        self.satellite = Satellite.objects.create(
            name='PACE',
            norad_id=12345,
            satellite_type='Observation',
            description='Engineered to explore the Universe.'
        )
        self.location = Location.objects.create(
            name='South Pole',
            latitude=0.0,
            longitude=0.0,
            altitude_m=0.0
        )
        self.dt = datetime.datetime(1990, 8, 1, 5, 8, 0, tzinfo=datetime.timezone.utc)

    def test_max_elevation_value_outside_0_is_rejected(self):
        data = {
            'satellite': self.satellite.id,  # type: ignore
            'location': self.location.id,    # type: ignore
            'datetime': self.dt,
            'duration_seconds': 0,
            'max_elevation_deg': -1,
        }
        serializer = PassSerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_max_elevation_value_outside_90_is_rejected(self):
        data = {
            'satellite': self.satellite.id,  # type: ignore
            'location': self.location.id,    # type: ignore
            'datetime': self.dt,
            'duration_seconds': 0,
            'max_elevation_deg': 100,
        }
        serializer = PassSerializer(data=data)
        self.assertFalse(serializer.is_valid())
