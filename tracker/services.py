'''Handles external API calls to N2YO for satellite pass predictions.'''

import os
import requests
import datetime
import logging

from tracker.models import Pass


logger = logging.getLogger(__name__)


def fetch_predicted_passes(satellite, location, days=5, min_elevation=10):
    logger.info(f'Fetching passes for satellite {satellite.norad_id} at location {location.name}')
    api_key = os.getenv('N2YO_API_KEY')
    url = (
        f'https://api.n2yo.com/rest/v1/satellite/visualpasses/'
        f'{satellite.norad_id}/{location.latitude}/{location.longitude}/'
        f'{location.altitude_m}/{days}/{min_elevation}'
        f'&apiKey={api_key}'
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        logger.error(f'N2YO API request timed out for satellite {satellite.norad_id}')
        raise
    except requests.exceptions.RequestException as e:
        logger.error(f'N2YO API request failed: {e}')
        raise
    logger.info(f'Successfully fetched {len(response.json().get("passes", []))} passes')
    return response.json()


def save_predicted_passes(satellite, location, days=5, min_elevation=10):
    data = fetch_predicted_passes(satellite, location, days, min_elevation)
    passes = data.get('passes', [])
    created = []
    for p in passes:
        dt = datetime.datetime.fromtimestamp(p['startUTC'], tz=datetime.timezone.utc)
        pass_event = Pass.objects.create(
            satellite=satellite,
            location=location,
            datetime=dt,
            duration_seconds=p['duration'],
            max_elevation_deg=p['maxEl'],
        )
        created.append(pass_event)
    logger.info(f'Saved {len(created)} predicted passes for {satellite.name}')
    return created
