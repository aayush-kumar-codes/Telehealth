import imp
from pickle import TRUE
from django.db import models
from user.models import(
    Doctor,
    CustomUser
)


# Create your models here.

class Slot(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="doctorSlot",null=True,blank=True)
    time_from=models.TimeField()
    time_to=models.TimeField()
    is_availavle=models.BooleanField(default=False)

class Bookings(models.Model):
    slot=models.ForeignKey(Slot,on_delete=models.CASCADE,related_name="bookingSlot")
    patient=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Patient")
    is_active=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)