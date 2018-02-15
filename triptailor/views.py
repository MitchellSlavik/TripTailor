from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip
# Create your views here.
def home(request):
    data = {
        "userLoggedIn":False,
        "searchResults":Trip.objects.all()
    }
    return render(request,"triptailor/home.html",data)

def profile(request):
    data = {
        'hello' : "hello colin"
    }
    return render(request,"triptailor/profile.html",data)

def trips(request):
    data = {
        'hello' : "hello jonathan"
    }
    return render(request,"triptailor/trips.html",data)

def dashboard(request):
    data = {
        'hello' : "hello carly"
    }
    return render(request,"triptailor/dashboard.html",data)

def login(request):
    data = {
        "userLoggedIn":False,
    }
    return render(request,"triptailor/login.html",data)

def createUserPage(request):
    data = {
        "userLoggedIn":False,
    }
    return render(request,"triptailor/create-user.html",data)

def createTrip(request):
    data = {
        "userLoggedIn":False,
    }
    return render(request,"triptailor/create-trip.html",data)