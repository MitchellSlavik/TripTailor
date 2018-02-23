from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip
from .models import Guide
from django.db.models import Q
# Create your views here.
def home(request):
    data = {
        "userLoggedIn":False,
        "searchResults":Trip.objects.all()
    }
    return render(request,"triptailor/home.html",data)

def searchTrip(request):
    if request.method == 'GET':
        searchcriteria = request.GET.get('search_criteria')
        startrange = request.GET.get('start_range')
        endrange = request.GET.get('end_range')
        try:
            data = {
                "searchResults":Trip.objects.filter(name__icontains=searchcriteria) |
                Trip.objects.filter(maxNumTravelers__icontains=searchcriteria) |
                Trip.objects.filter(description__icontains=searchcriteria) |
                Trip.objects.filter(cost__icontains=searchcriteria)
                #Trip.objects.filter(date__range=[startrange, endrange])
            }
        except Trip.DoesNotExist:
            data = {"searchResults": None}
        return render(request,"triptailor/search-results.html",data)
    else:
        return render(request,"home.html",{})
    
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
    if(request.method == 'POST'):
        
        return HttpResponse('') #sends ok for redirect will add id of new page eventually
    else:
        if request.user.is_authenticated:
            return render(request,"triptailor/create-trip.html",{})
        else:
            return render(request,"triptailor/home.html",{})
