from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from . import models
from datetime import date
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.serializerfields import PhoneNumberField




class UserRegisterSerializer(serializers.ModelSerializer):
    queryset=models.CustomUser.objects.all()
    phoneNumber=PhoneNumberField(
            required=False ,validators=[UniqueValidator(queryset=queryset)]
            )
    email = serializers.EmailField(
            required=False ,validators=[UniqueValidator(queryset=queryset)]
            )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = models.CustomUser
        fields = ("email","password", "password2","name","phoneNumber")
        extra_kwargs = {
            'name': {'required': True, 'allow_blank': False},
            }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        name = validated_data.pop("name", None)
        phoneNumber = validated_data.pop("phoneNumber", None)
        user = models.CustomUser.objects.create(
            email=email, 
            phoneNumber=phoneNumber,
            password=make_password(password),
            name=name,
        )
        return user

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance

class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Speciality
        fields = ["type"]

class DoctorProfileSerializer(serializers.ModelSerializer):
    speciality=serializers.SerializerMethodField()
    class Meta:
        model=models.Doctor
        fields='__all__'
            
        extra_kwargs={"doctor":{"required":False}}
    def get_speciality(self,obj):
        object=models.Speciality.objects.filter(doctor=obj)
        serializer=SpecialitySerializer(object,many=True).data
        specObj=[]
        for data in serializer:
            specObj.append(data["type"])
        return specObj

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ("email","phoneNumber","name","role")