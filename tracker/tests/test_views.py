'''Unit tests for tracker views.'''

import datetime

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from tracker.models import Location, Satellite, Pass


class SatelliteViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
    
    def test_unauthenticated_request_returns_401_response(self):
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get('/api/v1/satellites/')
        self.assertEqual(response.status_code, 401)  # type: ignore

    def test_authenticated_request_returns_200_response(self):
        response = self.client.get('/api/v1/satellites/')
        self.assertEqual(response.status_code, 200)

    def test_create_satellite_returns_201_response(self):
        data = {
            'name': 'JWST',
            'norad_id': 99999,
            'satellite_type': 'Observation',
            'description': 'James Webb Space Telescope.'
        }
        response = self.client.post('/api/v1/satellites/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_satellite_filter_returns_correct_type(self):
        Satellite.objects.create(
            name='JWST',
            norad_id=99999,
            satellite_type='Observation',
            description='James Webb Space Telescope.'
        )
        Satellite.objects.create(
            name='Helix',
            norad_id=88888,
            satellite_type='Espionage',
            description='Top-secret.'
        )
        response = self.client.get('/api/v1/satellites/?satellite_type=Observation')
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(len(response.data['results']), 1)  # type: ignore
        self.assertEqual(response.data['results'][0]['satellite_type'], 'Observation')  # type: ignore


class PassViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        location = Location.objects.create(
            name='Test Location',
            latitude=0.0,
            longitude=0.0,
            altitude_m=0.0
        )
        satellite = Satellite.objects.create(
            name='Test Satellite',
            norad_id=12345,
            satellite_type='Test type',
            description='Test description'
        )
        dt_1 = datetime.datetime(2023, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        Pass.objects.create(
            satellite=satellite,
            location=location,
            datetime=dt_1,
            duration_seconds=0,
            max_elevation_deg=0.0,
        )
        dt_2 = datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
        Pass.objects.create(
            satellite=satellite,
            location=location,
            datetime=dt_2,
            duration_seconds=0,
            max_elevation_deg=0.0,
        )

    def test_date_filter_returns_correct_pass_event(self):
        response = self.client.get('/api/v1/passes/?start_date=2024-01-01&end_date=2024-12-31')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)  # type: ignore
        self.assertEqual(response.data['results'][0]['datetime'], '2024-01-01T00:00:00Z')  # type: ignore
