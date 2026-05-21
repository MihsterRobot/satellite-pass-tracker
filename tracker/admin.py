'''Registers tracker models with the Django admin interface.'''

from django.contrib import admin
from .models import Location, Satellite, Pass


admin.site.register(Location)
admin.site.register(Satellite)
admin.site.register(Pass)
