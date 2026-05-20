'''Unit tests for tracker models.'''

import datetime

from django.test import TestCase

from tracker.models import Location, Satellite, Pass


class LocationModelTest(TestCase):
    def test_str_returns_name(self):
        location = Location.objects.create(
            name='Test Location',
            latitude=0.0,
            longitude=0.0,
            altitude_m=0.0
        )
        self.assertEqual(str(location), 'Test Location')


class SatelliteModelTest(TestCase):
    def test_str_returns_name(self):
        satellite = Satellite.objects.create(
            name='Test Satellite',
            norad_id=12345,
            satellite_type='Test type',
            description='Test description'
        )
        self.assertEqual(str(satellite), 'Test Satellite')


class PassModelTest(TestCase):
    def test_str_returns_expected_string(self):
        satellite = Satellite.objects.create(
            name='Test Satellite',
            norad_id=12345,
            satellite_type='Test type',
            description='Test description'
        )
        location = Location.objects.create(
            name='Test Location',
            latitude=0,
            longitude=0,
            altitude_m=0.0
        )
        dt = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        pass_event = Pass.objects.create(
            satellite=satellite,
            location=location,
            datetime=dt,
            duration_seconds=0,
            max_elevation_deg=0.0,
        )
        self.assertEqual(str(pass_event), f'Test Satellite over Test Location on {dt}')
