from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from user.manager import CustomUserManager
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField




class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True,null=True,blank=True)
    phoneNumber=PhoneNumberField(null=True,unique=True,blank=True)
    name=models.CharField(max_length=200)
    username=None
    ROLE_CHOICE=(
        ("Admin","Admin"),
        ("Doctor","Doctor"),
        ("User","User")
    )

    role = models.CharField(choices=ROLE_CHOICE,default='User', max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phoneNumber',]

    objects = CustomUserManager()

    is_verified=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True,null=True,blank=True)
    is_staff = models.BooleanField(default=False,null=True,blank=True)
    is_superuser = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        if self.email!=None:
            return self.email
        else:
            return str(self.phoneNumber)



class Doctor(models.Model):
    doctor=models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name="Doctor",null=True,blank=True)
    abount=models.TextField(max_length=2000)
    profile_image=models.ImageField(upload_to='profile',null=True,blank=True)
    LANGUAGE_TYPE=(
        ("Arabic","Arabic"),
        ("English","English"),
        ("Romania","Romania"),
    )
    language=models.CharField(max_length=20,choices=LANGUAGE_TYPE,default="English")
    CONSULTATION_TYPE=(
        ("Clinical","Clinical"),
        ("Online","Online",)
    )
    consultation_type=models.CharField(max_length=20,choices=CONSULTATION_TYPE)
    consultation_price=models.DecimalField(max_digits=100000,decimal_places=2)
    GENDER=(
        ("Male","Male"),
        ("Female","Female"),
        ("Other","Other"),
    )
    gender=models.CharField(max_length=20,choices=GENDER)
    insurance_company=models.CharField(max_length=500)
    insurance_number=models.CharField(max_length=20)
    available_week=models.CharField(max_length=50)
    available_time=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)

class Speciality(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,related_name="doctorSpeciality")
    type=models.CharField(max_length=100)
