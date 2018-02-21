from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path('',views.home),
    path('searchtrip/',views.searchTrip, name='searchTrip'),
    path('profile/',views.profile),
    path('trips/',views.trips),
    path('dashboard/',views.dashboard),
    path('login/',views.login),
    path('createuser/',views.createUserPage),
    path('createtrip/',views.createTrip, name='createtrip'),
    path('postnewtrip/',views.postNewTrip,name="postTrip"),
]
