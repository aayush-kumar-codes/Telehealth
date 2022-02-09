from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Bookings)
admin.site.register(models.Slot)