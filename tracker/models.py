'''Each model represents a table in the database.'''

from django.db import models


class Location(models.Model):
    '''Represents a ground-based observation location.'''
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField()

    def __str__(self):
        # Return a string representation of the object.
        return self.name


class Satellite(models.Model):
    '''Represents an individual satellite.'''
    name = models.CharField(max_length=100)
    norad_id = models.IntegerField()
    satellite_type = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Pass(models.Model):
    '''Represents a satellite pass event over a given location.'''
    satellite = models.ForeignKey(Satellite, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    duration_seconds = models.IntegerField()
    max_elevation = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    # Django automatically generates plural names for models by appending an 's'; 'Pass' became
    # 'Passs' instead of 'Passes'. The line below corrects this issue.
    class Meta:
        verbose_name_plural = 'Passes'

    def __str__(self):
        return f'{self.satellite.name} over {self.location.name} on {self.datetime}'
