<<<<<<< HEAD
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home),
    path('profile/',views.profile),
    path('trips/',views.trips),
    path('dashboard/',views.dashboard),
    path('login/',views.login)
]
=======
from django.urls import path

from . import views


urlpatterns = [
    path('',views.home),
    path('profile/',views.profile),
    path('trips/',views.trips),
    path('dashboard/',views.dashboard),
    path('login/',views.login)
]
>>>>>>> da2ae40e673dada716c3deeb8a77b00b73c3d93c
