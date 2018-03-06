from django.contrib import admin

# Register your models here.
from . import models
admin.site.register(models.Guide)
admin.site.register(models.Traveler)
admin.site.register(models.Ticket)
admin.site.register(models.Trip)
admin.site.register(models.Location)
admin.site.register(models.Category)
admin.site.register(models.TripPicture)