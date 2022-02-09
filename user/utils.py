
from . import models
from django.db.models import Q
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserDetailsSerializer
from django.core.validators import validate_email
from phonenumber_field.validators import validate_international_phonenumber

def get_response(code,message,data={}):
    if code>=200:
        status=False
    else:
        status=True
    return {
        "success":status,
        "status":code,
        "message":message,
        "result":data,
    }

def authenticate(self, username, password):
        try:
            user = models.CustomUser.objects.get(
                Q(email=username) | Q(phoneNumber=username)
            )
        except models.CustomUser.DoesNotExist:
            return None
        return user if user.check_password(password) else None


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    serializer=UserDetailsSerializer(user).data
    return {
        'token_type':'Bearer',
        'expiresIn': '3600',
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user_details':serializer
    }

def valid_email(username):
    try:
        validate_email(username)
        return True
    except:
        return False

def valid_phone(username):
    try:
        validate_international_phonenumber(username)
        return True
    except:
        return False
