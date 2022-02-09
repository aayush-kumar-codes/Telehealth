from dataclasses import field
from rest_framework import serializers
from . import models
from datetime import date
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField




class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Bookings
        fields='__all__'


class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Slot
        fields='__all__'
    extra_kwrgs={
        "doctor":{"required":False}}
        