from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('', views.home),
    path('searchtrip/', views.searchTrip, name='searchTrip'),
    path('profile/', views.profile, name="profile"),
    path('trips/', views.trips),
    path('dashboard/', views.dashboard),
    path('register/', views.traveler_register, name="traveler_register"),
    path('login/', views.traveler_login, name="traveler_login"),
    path('logout/', views.traveler_logout),
    path('createuser/', views.createUserPage),
    path('createtrip/', views.createTrip, name='createtrip'),
    path('postnewtrip/', views.postNewTrip, name="postTrip"),
]
