from django.urls import path
from . import views

urlpatterns = [
    path('get_my_bookings/', views.MybookingsView.as_view()),
    path('get_my_bookings/<int:pk>/', views.MybookingsView.as_view()),

    path('get_my_availability_slots/', views.SetSlotView.as_view()),
    path('set_my_availavle_slot/<int:pk>/', views.SetSlotView.as_view()),

    path('patient/', views.PatientBookingView.as_view()),
    path('get_my_patients/', views.MyPatientListView.as_view()),
]