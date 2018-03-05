from django.contrib import admin
from django.urls import path, include

from . import views
from . import dashboardViews


urlpatterns = [
    path('',views.home, name="home"),
    path('searchtrip/',views.searchTrip, name='searchTrip'),
    path('trips/',views.trips),
    path('profile/', views.profile, name="profile"),
    path('trips/', views.trips),
    path('register/', views.traveler_register, name="traveler_register"),
    path('login/', views.traveler_login, name="traveler_login"),
    path('guide_register/', views.guide_register, name="guide_register"),
    path('guide_login/', views.guide_login, name="guide_login"),
    path('logout/', views.user_logout),
    path('createuser/', views.createUserPage),
    path('dashboard/', dashboardViews.view_dashboard, name='view_dashboard'),
    path('dashboard/create/', dashboardViews.create_trip, name='create_trip'),
    path('dashboard/edit/<int:trip_id>', dashboardViews.edit_trip, name='edit_trip'),
    path('dashboard/delete/', dashboardViews.delete_trip, name='delete_trip')
]
