'''Each model represents a table in the database.'''

from django.db import models


class Location(models.Model):
    '''Represents a ground-based observation location.'''
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude_m = models.FloatField(verbose_name='Altitude (m)')

    def __str__(self):
        # Return a string representation of the object.
        return self.name


class Satellite(models.Model):
    '''Represents an individual satellite.'''
    name = models.CharField(max_length=100)
    norad_id = models.IntegerField()
    satellite_type = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Pass(models.Model):
    '''Represents a satellite pass event over a given location.'''
    satellite = models.ForeignKey(Satellite, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    duration_seconds = models.IntegerField()
    max_elevation_deg = models.FloatField(verbose_name='Max elevation (°)')
    notes = models.TextField(blank=True, null=True)

    # Django automatically generates plural names by appending an 's'; 'Pass' became
    # 'Passs' instead of 'Passes'. 'ordering' ensures consistent pagination results.
    class Meta:
        verbose_name_plural = 'Passes'
        ordering = ['datetime']

    def __str__(self):
        return f'{self.satellite.name} over {self.location.name} on {self.datetime}'
