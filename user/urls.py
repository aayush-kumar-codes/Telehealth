from django.urls import path
from . import views

urlpatterns = [
    path('sign_up/', views.RegisterView.as_view()),
    path('sign_in/', views.Signin.as_view()),

    path('get_my_accoount/', views.ProfileView.as_view()),
]