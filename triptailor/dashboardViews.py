from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Prefetch
from .models import *

from datetime import datetime
import json

@permission_required('triptailor.is_guide')
def view_dashboard(request):
    prefetch = Prefetch("locations", queryset=Location.objects.all().order_by('sequence'), to_attr="locs")
    
    pastTrips = request.user.guide.trips.prefetch_related(prefetch).filter(date__lt=datetime.today()).annotate(location_count=Count('locations')).order_by('-date')
    upcomingTrips = request.user.guide.trips.prefetch_related(prefetch).filter(date__gte=datetime.today()).annotate(location_count=Count('locations')).order_by('-date')
    data = {
        "pastTrips": pastTrips,
        "upcomingTrips": upcomingTrips
    }

    return render(request, 'triptailor/dashboard.html', data)

@permission_required('triptailor.is_guide')
def view_trip(request, trip_id):
    try:
        trip = Trip.objects.get(pk=trip_id)

        if trip.guide.user.id == request.user.id:
            return render(request, 'triptailor/dashboard-trip.html')
        else:
            return redirect('view_dashboard')
    except Trip.DoesNotExist:
        return redirect('view_dashboard')

    

@permission_required('triptailor.is_guide')
def delete_trip(request):
    if request.method == 'GET':
        data = request.GET.dict()

        id = data.get('id', '')

        if id != '':
            trip = Trip.objects.get(pk=id)

            if request.user.id == trip.guide.user.id or request.user.is_staff:
                trip.delete()

    return redirect('view_dashboard')



@permission_required('triptailor.is_guide')
def create_trip(request):
    if request.method == 'POST':
        form = request.POST
        form_data = form.dict()

        form_data['locations'] = json.loads(form_data['locations'])
        print(form_data)

        #basic server side validation to make sure all our fieds are present
        #can skip major stuff since most processing was done client side
        create_form_elements = ['name','cost','maxTravelers','date','locations','description']
        #guide_obj = Guide.objects.get(User.objects.get(username=request.user).id)
        if all(item in form_data for item in create_form_elements):
            #fix date?
            t = Trip(name = form_data['name'], cost = form_data['cost'], maxNumTravelers = form_data['maxTravelers'],
            description = form_data['description'],date = form_data['date'], guide_id =request.user.id)
            t.save()
            seq_count = 0
            for place in form_data['locations']: #iterate over all locations and add them to DB
                location = Location(name= place['address'], sequence = seq_count, trip=t,description=place['placeId'])
                location.save()
                seq_count +=1

        return HttpResponse({'status':200})
    else:
        return render(request, "triptailor/create-trip.html", {})


@permission_required('triptailor.is_guide')
def post_new_trip(request):
    if request.method == 'POST' and request.user.is_authenticated:
        # form = DinnerForm(request.POST)
        # if form.is_valid():
            # name = form.cleaned_data['name']
            # text = form.cleaned_data['text']
            # query = Dinner(name = name , text = text)
            # query.save()
        print('hello world')
    else:
        return(request, "triptailor/home.html", {})