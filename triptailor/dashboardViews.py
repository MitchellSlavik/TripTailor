from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count, Prefetch
from .models import *

from datetime import datetime
import json

@permission_required('triptailor.is_guide')
def myTrips(request):
    current_user = request.user
    prefetch_pictures = prefetch = Prefetch("images", queryset=TripPicture.objects.all().order_by('sequence'), to_attr="imgs")
    try:
        data = {
            "mytrips":Trip.objects.prefetch_related(prefetch_pictures).filter(guide__user__username__icontains=current_user)
        }
    except Trip.DoesNotExist:
        data = {"searchResults": None}
    return render(request, "triptailor/myTrips.html", data)
    
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
def edit_trip(request, trip_id):
    if request.method == 'POST':
        form_data = request.POST.dict()

        form_data['locations'] = json.loads(form_data['locations'])

        create_form_elements = ['name','cost','maxTravelers','date','locations','description']
        
        if all(item in form_data for item in create_form_elements):
            trip = Trip.objects.get(pk=trip_id)

            trip.name = form_data['name']
            trip.cost = form_data['cost']
            trip.maxNumTravelers = form_data['maxTravelers']
            trip.date = form_data['date']
            trip.description = form_data['description']

            trip.save()

            trip.locations.all().delete()

            seq_count = 0
            for place in form_data['locations']:
                if(place != None):
                    location = Location(address= place['address'], sequence = seq_count, trip=trip,placeId=place['placeId'])
                    location.save()
                    seq_count +=1

            trip.images.all().delete()

            imageUrls = json.loads(form_data['images'])

            seq_count = 0
            if(len(imageUrls)):
                for url in imageUrls:
                    if(url != None):
                        picture = TripPicture(image=url,sequence=seq_count,trip=trip)
                        picture.save()
                        seq_count += 1
            
            return HttpResponse({'status':200})
        else:
            return HttpResponse({'status':500})
    else:
        try:
            trip = Trip.objects.get(pk=trip_id)

            if trip.guide.user.id == request.user.id:

                locations = Location.objects.filter(trip__id=trip_id).order_by('sequence')
                images = TripPicture.objects.filter(trip__id=trip_id).order_by('sequence')

                data = {
                    "trip": trip,
                    "locations": locations,
                    "images": images
                }

                return render(request, 'triptailor/dashboard-edit.html', data)
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
        create_form_elements = ['name','cost','maxTravelers','date','locations','description','images']
        #guide_obj = Guide.objects.get(User.objects.get(username=request.user).id)
        if all(item in form_data for item in create_form_elements):
            #fix date?
            t = Trip(name = form_data['name'], cost = form_data['cost'], maxNumTravelers = form_data['maxTravelers'],
            description = form_data['description'],date = form_data['date'], guide_id =request.user.id)
            t.save()
            seq_count = 0
            for place in form_data['locations']: #iterate over all locations and add them to DB
                location = Location(address= place['address'], sequence = seq_count, trip=t,placeId=place['placeId'])
                location.save()
                seq_count +=1
            # seq = 0
            # if(len(request.FILES)>0): #if we have some images let's add them to our Trip!
            #     for file in request.FILES:
            #         print(file.name)
            #         # https://simpleisbetterthancomplex.com/tutorial/2016/08/01/how-to-upload-files-with-django.html
            #         # https://stackoverflow.com/questions/1308386/programmatically-saving-image-to-django-imagefield
            #         fs = FileSystemStorage()
            #         image_name = fs.save(file.name,file)
            #         image_url_on_server = fs.url(image_name)

            #         image = TripPicture(image=image_url_on_server,sequence=seq,trip=t)
            #         image.save()
            #         seq +=1
            imageUrls = json.loads(form_data['images'])
            seq = 0
            if(len(imageUrls)):
                for url in imageUrls:
                    image = TripPicture(image=url,sequence=seq,trip=t)
                    image.save()
                    seq +=1
            return HttpResponse({'status':200})
        else:
            return HttpResponse({'status':404,'message':"element in posted data was missing"})
    else:
        return render(request, "triptailor/dashboard-create.html", {})
