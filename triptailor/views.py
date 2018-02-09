from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    data = {}
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
        'hello' : "hello friend"
    }
    return render(request,"triptailor/login.html",data)
