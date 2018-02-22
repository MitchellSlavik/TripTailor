from django.shortcuts import render
from django.http import HttpResponse
from .models import Trip
from .models import Guide
from .models import Category
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
    #    startrange = request.GET.get('start_range')
    #    endrange = request.GET.get('end_range')
        try:
            data = {
                "searchResults":Trip.objects.filter(name__icontains=searchcriteria) |
                Trip.objects.filter(maxNumTravelers__icontains=searchcriteria) |
                Trip.objects.filter(description__icontains=searchcriteria) |
                Trip.objects.filter(cost__icontains=searchcriteria) |
                Trip.objects.filter(categories__name__icontains=searchcriteria)
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
    if request.user.is_authenticated:
        return render(request,"triptailor/create-trip.html",{})
    else:
        return(request,"triptailor/home.html",{})

def postNewTrip(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # form = DinnerForm(request.POST)
        # if form.is_valid():
            # name = form.cleaned_data['name']
            # text = form.cleaned_data['text']
            # query = Dinner(name = name , text = text)
            # query.save()
        print('hello world')
    else:
        return(request,"triptailor/home.html",{})