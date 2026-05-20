'''Unit tests for tracker models.'''

import datetime

from django.test import TestCase

from tracker.models import Location, Satellite, Pass


class LocationModelTest(TestCase):
    def test_str_returns_name(self):
        location = Location.objects.create(
            name='North Pole',
            latitude=45.0,
            longitude=90,
            altitude_m=100.0
        )
        self.assertEqual(str(location), 'North Pole')


class SatelliteModelTest(TestCase):
    def test_str_returns_name(self):
        satellite = Satellite.objects.create(
            name='PACE',
            norad_id=12345,
            satellite_type='Observation',
            description='Engineered to explore the Universe.'
        )
        self.assertEqual(str(satellite), 'PACE')


class PassModelTest(TestCase):
    def test_str_returns_expected_string(self):
        satellite = Satellite.objects.create(
            name='PACE',
            norad_id=12345,
            satellite_type='Observation',
            description='Engineered to explore the Universe.'
        )
        location = Location.objects.create(
            name='South Pole',
            latitude=0,
            longitude=0,
            altitude_m=100.0
        )
        dt = datetime.datetime(1990, 8, 1, 5, 8, 0, tzinfo=datetime.timezone.utc)
        pass_event = Pass.objects.create(
            satellite=satellite,
            location=location,
            datetime=dt,
            duration_seconds=60,
            max_elevation_deg=90,
        )
        self.assertEqual(str(pass_event), f'PACE over South Pole on {dt}')
