from django.contrib import admin
from django.urls import path, include

from . import views
from . import dashboardViews


urlpatterns = [
    path('',views.home, name="home"),
    path('aboutus/', views.aboutUs, name="aboutUs"),
    path('searchtrip/',views.searchTrip, name='searchTrip'),
    path('profile/', views.profile, name="profile"),
    path('profile/<int:guide_id>', views.guideProfile, name="guideProfile"),
    path('profile/mytrips', dashboardViews.myTrips, name="my_trips"),
    path('trip/<int:trip_id>', views.trip, name="view_trip"),
    path('register/', views.traveler_register, name="traveler_register"),
    path('login/', views.traveler_login, name="traveler_login"),
    path('guide_register/', views.guide_register, name="guide_register"),
    path('guide_login/', views.guide_login, name="guide_login"),
    path('logout/', views.user_logout),
    path('createuser/', views.createUserPage),
    path('dashboard/', dashboardViews.view_dashboard, name='view_dashboard'),
    path('dashboard/create/', dashboardViews.create_trip, name='create_trip'),
    path('dashboard/edit/<int:trip_id>', dashboardViews.edit_trip, name='edit_trip'),
    path('dashboard/delete/', dashboardViews.delete_trip, name='delete_trip'),
    path('purchaseTrip/<int:trip_id>/<int:openSpots>',views.purchaseTrip,name="purchase"),
    path('review/<int:trip_id>', views.review, name='review'),
]
