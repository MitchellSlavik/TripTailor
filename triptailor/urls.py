from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('searchtrip/',views.searchTrip, name='searchTrip'),
    path('trips/',views.trips),
    path('dashboard/',views.dashboard),
    path('createtrip/',views.createTrip, name='createtrip'),
    path('profile/', views.profile, name="profile"),
    path('register/', views.traveler_register, name="traveler_register"),
    path('login/', views.traveler_login, name="traveler_login"),
    path('guide_register/', views.guide_register, name="guide_register"),
    path('guide_login/', views.guide_login, name="guide_login"),
    path('logout/', views.user_logout),
    path('createuser/', views.createUserPage),
    path('createtrip/', views.createTrip, name='createtrip'),
]
