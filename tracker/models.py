'''Each model represents a table in the database.'''

from django.db import models


class Location(models.Model):
    '''Represents a ground-based observation location.'''
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()


class Satellite(models.Model):
    '''Represents an individual satellite.'''
    name = models.CharField(max_length=100)
    norad_id = models.IntegerField()
    satellite_type = models.CharField(max_length=100)
    description = models.TextField()


class Pass(models.Model):
    '''Represents a satellite pass event over a given location.'''
    satellite = models.ForeignKey(Satellite, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    duration_seconds = models.IntegerField()
    max_elevation = models.FloatField()
    notes = models.TextField(blank=True, null=True)
