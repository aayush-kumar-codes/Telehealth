from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from rest_framework import permissions
from rest_framework import status
from . import utils
from . import serializers
from . import models


# Create your views here.



class RegisterView(APIView):
    def post(self, request):
        username=request.data.get("emailOrPhone")
        data=request.data
        if not username:
            message="emailOrPhone field required"
            return Response(utils.get_response(400,message),status=status.HTTP_400_BAD_REQUEST)
        if utils.valid_email(username):
            data["email"]=username
        elif utils.valid_phone(username):
            data["phoneNumber"]=username
        else:
            message="please enter a valid email or phone"
            return Response(utils.get_response(400,message))

        serializer = serializers.UserRegisterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            message="created successfully"
            return Response(utils.get_response(200,message,serializer.data))
        message="field error"
        return Response(utils.get_response(400,message,serializer.errors)
                    ,status=status.HTTP_400_BAD_REQUEST
                    )


class Signin(APIView):
     def post(self, request):
        username=request.data.get("emailOrPhone")
        password=request.data.get("password")
        if username is None:
            message="emailOrPhone field required"
            return Response(utils.get_response(200,message),status=status.HTTP_200_OK)
        if password is None:
            message="password this field required"
            return Response(utils.get_response(400,message),status=status.HTTP_400_BAD_REQUEST)
        if models.CustomUser.objects.filter(Q(email=username)|Q(phoneNumber=username)).exists():
            user = utils.authenticate(
                self,username=username, password=request.data.get("password")
            )
            if user is not None:
                message="logged in successfully"
                return Response(utils.get_response(200,message,utils.get_token_for_user(user)),status.HTTP_200_OK)
            else:
                message="This password is incorrect, please try again"
                return Response(utils.get_response(401,message),status=status.HTTP_401_UNAUTHORIZED)
        message="email or phone does not exist"
        return Response(utils.get_response(400,message))

class ProfileView(APIView):
    permission_classes =[permissions.IsAuthenticated,]
    def get(self,request):
        object=models.Doctor.objects.filter(doctor=request.user)
        serializer=serializers.DoctorProfileSerializer(object,many=True).data
        message="doctor profile"
        return Response(utils.get_response(200,message,serializer),status=status.HTTP_200_OK)
    
    def post(self,request):
        data=request.data
        speciality=request.data.get("speciality")
        if speciality is None:
            message="speciality field required"
            return Response(utils.get_response(400,message))
        if models.Doctor.objects.filter(doctor_id=request.user.id).exists():
            message="profile already exist"
            return Response(utils.get_response(400,message),status=400)
        serializer=serializers.DoctorProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save(doctor=request.user,role="Doctor")
            for spec in speciality:
                models.Speciality.objects.create(doctor_id=request.user.Doctor.get().id,type=spec)
            message="profile created"
            return Response(utils.get_response(200,message,serializer.data),status=status.HTTP_201_CREATED)
        message="field error"
        return Response(utils.get_response(400,message,serializer.errors))

    def patch(self,request):
        try:
            object=models.Doctor.objects.get(doctor=request.user)
            serializer=serializers.DoctorProfileSerializer(object,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                message="profile updated"
                return Response(utils.get_response(200,message,serializer.data),status=status.HTTP_201_CREATED)
            message="field error"
            return Response(utils.get_response(400,message,serializer.errors))
        except:
            message="profile not found"
            return Response(utils.get_response(404,message))