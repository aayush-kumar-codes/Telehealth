from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status
from user.utils import get_response
from . import serializers
from . import models
from user.models import(
    Doctor,
    CustomUser,
)
from user.serializers import UserDetailsSerializer
# Create your views here.


class MybookingsView(APIView):
    permission_classes =[permissions.IsAuthenticated,]
    def get(self,request):
        try:
            object=models.Bookings.objects.filter(slot__doctor=request.user.Doctor.get())
            serializer=serializers.BookingSerializer(object,many=True).data
            message="doctor booking"
            return Response(get_response(200,message,serializer),status=status.HTTP_200_OK)
        except:
            message="not found"
            return Response(get_response(400,message))
    def patch(self,request,pk):
        try:
            object=models.Bookings.objects.get(slot__doctor=request.user.Doctor.get(),pk=pk)
            serializer=serializers.BookingSerializer(object,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                message="booking updated"
                return Response(get_response(200,message,serializer.data),status=status.HTTP_201_CREATED)
            message="field error"
            return Response(get_response(400,message,serializer.errors))
        except:
            message="booking not found"
            return Response(get_response(404,message))
       
class SetSlotView(APIView):
    permission_classes =[permissions.IsAuthenticated,]
    def get(self,request):
        pk=request.GET.get("id")
        is_availavle=request.GET.get("is_availavle")
        slotObject=models.Slot.objects.filter(doctor=request.user.Doctor.get())
        if slotObject.exists():
            if is_availavle is not None:
                object=slotObject.filter(is_availavle=is_availavle)
            elif pk is not None:
                object=slotObject.filter(pk=pk)
            else:
                object=slotObject
            serializer=serializers.SlotSerializer(object,many=True).data
            message="slot list"
            return Response(get_response(200,message,serializer))
    def post(self,request):
        time_from=request.data.get("time_from")
        time_to=request.data.get("time_to")
        time_check=models.Slot.objects.filter(doctor=request.user.Doctor.get())
        check_1 = time_check.filter(time_from__lte=time_from, time_to__gte=time_from).exists()
        check_2 = time_check.filter(time_from__lte=time_to, time_to__gte=time_to).exists()
        check_3 = time_check.filter(time_from__gte=time_from, time_to__lte=time_to).exists()
        if check_1 or check_2 or check_3:
            message="no slot avaliable"
            return Response(get_response(200,message))
        serializer=serializers.SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor=request.user.Doctor.get(),is_availavle=True)
            message="slot created"
            return Response(get_response(200,message,serializer.data),status=status.HTTP_201_CREATED)
        message="field error"
        return Response(get_response(400,message,serializer.errors),status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        try:
            object=models.Slot.objects.get(doctor=request.user.Doctor.get(),pk=pk)
            serializer=serializers.SlotSerializer(object,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                message="slot updated"
                return Response(get_response(200,message,serializer.data),status=status.HTTP_201_CREATED)
            message="field error"
            return Response(get_response(400,message,serializer.errors),status=status.HTTP_400_BAD_REQUEST)
        except:
            message="slot not found"
            return Response(get_response(404,message))
       


class PatientBookingView(APIView):
    permission_classes =[permissions.IsAuthenticated,]
    def get(self,request):
        object=models.Bookings.objects.filter(patient=request.user)
        if object.exists():
            serializer=serializers.BookingSerializer(object,many=True).data
            message="booking info"
            return Response(get_response(200,message,serializer))
        message="booking not found"
        return Response(get_response(404,message))

    def post(self,request):
        doctor=request.data.get("doctor")
        slot=request.data.get("slot")
        if slot is None:
            message="slot field required"
            return Response(get_response(400,message))
        allObjects=models.Slot.objects.filter(doctor=doctor,pk=slot)
        if doctor is None:
            message="doctor field required"
            return Response(get_response(400,message))
        if allObjects.exists():
            checkSlot=allObjects.filter(is_availavle=False)
            if checkSlot.exists():
                message="no slot avaliable"
                return Response(get_response(200,message))
            data=request.data
            data["patient"]=request.user.id
            serializer=serializers.BookingSerializer(data=request.data)
            if serializer.is_valid():
                obj=serializer.save(is_active=True)
                models.Slot.objects.filter(pk=obj.slot.id).update(is_availavle=False)
                message="booking confirm"
                return Response(get_response(200,message,serializer.data))
            message="field error"
            return Response(get_response(400,message,serializer.errors))
        message="doctor details not found"
        return Response(get_response(404,message))


class MyPatientListView(APIView):
    permission_classes =[permissions.IsAuthenticated,]
    def get(self,request):
        try:
            object=models.Bookings.objects.filter(slot__doctor=request.user.Doctor.get()).values_list("patient",flat=True)
            userObj=CustomUser.objects.filter(pk__in=object)
            serializer=UserDetailsSerializer(userObj,many=True).data
            message="Patient info"
            return Response(get_response(200,message,serializer))
        except:
            message="booking not found"
            return Response(get_response(404,message))
