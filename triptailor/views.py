from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import *
from .forms import UserForm, TravelerProfileForm, GuideProfileForm
from django.db.models import Q, Prefetch

import json

# Create your views here.

from operator import itemgetter

def home(request):
    data = {
        "userLoggedIn": False,
        "searchResults": Trip.objects.all()
    }
    return render(request, "triptailor/home.html", data)

def aboutUs(request):
    data = {
        
    }
    return render(request, "triptailor/aboutUs.html", data)

def searchTrip(request):
    if request.method == 'GET':
        searchcriteria = request.GET.get('search_criteria')
        prefetch_pictures = prefetch = Prefetch("images", queryset=TripPicture.objects.all().order_by('sequence'), to_attr="imgs")
    #    startrange = request.GET.get('start_range')
    #    endrange = request.GET.get('end_range')
        try:
            data = {
                "searchResults":Trip.objects.prefetch_related(prefetch_pictures).filter(Q(name__icontains=searchcriteria) |
                Q(maxNumTravelers__icontains=searchcriteria) | Q(description__icontains=searchcriteria) |
                Q(cost__contains=searchcriteria) | Q(categories__name__icontains=searchcriteria) |
                Q(guide__user__username__icontains=searchcriteria))
                #Trip.objects.filter(date__range=[startrange, endrange])
            }
        except Trip.DoesNotExist:
            data = {"searchResults": None}
        return render(request, "triptailor/search-results.html", data)
    else:
        return render(request, "home.html", {})


@permission_required("triptailor.is_traveler")
def profile(request):
    current_user = request.user
    prefetch_pictures = Prefetch("images", queryset=TripPicture.objects.all().order_by('sequence'), to_attr="imgs")
    myTickets = Ticket.objects.filter(traveler__user__username__icontains=current_user)
    myTicketTripIds = [e.trip.id for e in myTickets]

    myTripsWithPictures = Trip.objects.prefetch_related(prefetch_pictures).filter(pk__in=myTicketTripIds)
    try:
        data = {
            "mytrips": myTripsWithPictures,
            "numtrips": len(myTripsWithPictures)
        }
    except Trip.DoesNotExist:
        data = {"searchResults": None}
    return render(request, "registration/profile.html", data)


def trip(request,trip_id=1):
    #if the requested method is a getter, display the trip
    if request.method == 'GET':
        #get our revelent trip object
        trip = Trip.objects.get(id=trip_id)
        data = {} #init data object so we can package our data
        if(len(trip.name)>0):
            #put all the trip Object info in data
            data['trip_id'] = trip_id
            data['name'] = trip.name
            data['cost'] = trip.cost
            data['maxPeople'] = trip.maxNumTravelers
            data['date'] = trip.date
            data['description'] = trip.description
            

            #gather Guide information
            guideObject = Guide.objects.get(pk=trip.guide)
            #if our trip exists let's add it to the data.
            if(guideObject!=None):
                data['guideName'] = guideObject.user.first_name + " " + guideObject.user.last_name
                data['guideUserName'] = guideObject.user.username
                #Rating will go here
            else:
                render(request,"triptailor/404.html",{"message":"Guide on trip: {} doesn't exist!!".format(trip.name)})

            #gather trip location list for Google Maps
            locationObjects = Location.objects.filter(trip=trip.id)
            locations = [] #init locations object so we can fill it in our loop
            
            if(len(locationObjects)>0):
                #dank quality control check
                locations = [{"address": loc.address , "placeId": loc.placeId, "sequence":loc.sequence+1} for loc in locationObjects]
                #sort our locations by their sequence attribute to display them in order
                locations_sorted = sorted(locations,key=itemgetter('sequence')) 
                locations_JSON = json.dumps(locations_sorted)
                data['locations'] = locations_sorted
                data['locations_JSON'] = locations_JSON
                data['num_stops'] = len(locationObjects) +1
            else:
                return render(request,"triptailor/404.html",{"message":"Malformed Trip object. Length of locations are 0","error_object":locationObjects},)

            data['photos'] = getTripPhotoUrls(trip_id)

            data['open'], data['spotsOpen'] = getTripSpotStatus(trip_id)

        else:
            return render(request,"triptailor/404.html",{"message":"Trip doesn't exist yo!"})
        return render(request,"triptailor/trip.html",data)
    elif request.method == 'POST':
        #if its a post we're interested in processing the data
        return redirect(reverse('purchase',kwargs={"trip_id":trip_id}))


def getTripPhotoUrls(tripId):
    
    #grab our trip from the DB
    t = Trip.objects.get(pk=tripId)

    #gather trip photos from their DB objects
    photoObjects = TripPicture.objects.filter(trip=t)
    photoUrls = [photo.image for photo in photoObjects]
            
    #testing / handling for no photos
    if (len(photoUrls)==0):                         #default photo
        photoUrls = ['https://static.boredpanda.com/blog/wp-content/uploads/2014/10/national-geographic-photo-contest-2014-photography-15.jpg'
        ,'https://www.planwallpaper.com/static/images/7004579-cool-hd-wallpapers.jpg']
    
    return photoUrls


def getTripSpotStatus(tripId):
    #gather max amount of people
    t = Trip.objects.get(id=tripId)
    maxPeople = t.maxNumTravelers

    #gather all tickets (ie purchased tickets) and compare attendees to max attendes to determine if trip is open
    tickets = Ticket.objects.filter(trip=t)
    totalTravelers = 0
    #get total amount of travelers
    for ticket in tickets:
        totalTravelers += ticket.num_travelers
    #if we have spots available set open to true
    openTruthy = maxPeople>totalTravelers
    #show how many spots are open to the user
    spotsOpen = maxPeople - totalTravelers

    return openTruthy,spotsOpen


def purchaseTrip(request,trip_id=1,openSpots=1):
    if(hasattr(request.user,'traveler')):
        if (request.method == "GET"):
            #define an object to be sent back to page with data
            pageData = {}   

            #get our relevant trip so we can parse back its price and other needed infos
            tripData = Trip.objects.get(pk=trip_id) 

            #recycle our old data into this page (id and openSpots) for form POST
            pageData['trip_id'] = trip_id
            pageData['openSpots'] = openSpots
            
            #if our trip exists let's grab all the necessary data and put it in our pageData
            if(tripData.name):
                pageData['price'] = str(tripData.cost)
                pageData['name'] = tripData.name
                pageData['date'] = tripData.date.strftime("%A, %B %d")
                pageData['description'] = tripData.description
            else:
                return render("triptailor/404.html",{"message":"tripData was missing name and is most likely null"})   
            
            #everything is packaged, let's return our template and data!
            return render(request,"triptailor/purchaseTrip.html",pageData)

        #user has posted a form to our url. Let's process it and hopefully add them to the trip!
        elif (request.method == "POST"):
            #here we will take request.POST.get('numberTickets') and process a simple Ticket creation
            requestedTickets = int(request.POST.get('numberTickets'))

            #front end testing prohibits greater than available tickets, but we need to take into account for tickets that could be purchased after the page loads
            #after we test this, if there are no more spots available, return an error to user explaining that the trip is now full
            status, spots = getTripSpotStatus(trip_id)

            if(not status):
                return render("triptailor/404.html",{"message":"trip no longer available.. Sorry!"})

            #if all tests pass and user has sucessfully purchased their ticket (we don't put in purchase info in this demo)
            #then redirect them to their profile so they can see their trip has been added
            if(spots < requestedTickets):
                return render("triptailor/404.html",{"message":"Sorry, we no longer have enough tickets. Available tickets: {}.".format(spots)})

            #all things clear - create and save new element to DB and redirect user to profile
            new_ticket = Ticket(trip=Trip.objects.get(pk=trip_id),traveler=request.user.traveler,num_travelers=requestedTickets)
            new_ticket.save()  
            return redirect('profile')

    else:
        return redirect('traveler_login')


def createUserPage(request):
    data = {
        "userLoggedIn": False,
    }
    return render(request, "triptailor/create-user.html", data)


def traveler_register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and TravelerProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = TravelerProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Add user permissions
            permission = Permission.objects.get(name='Identifies as a Traveler')
            user.user_permissions.add(permission)


            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = TravelerProfileForm()

    # Render the template depending on the context.
    return render(request,
                  "registration/login.html",
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def guide_register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and GuideProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = GuideProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Add user permissions
            permission = Permission.objects.get(name='Identifies as a Guide')
            user.user_permissions.add(permission)


            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user
            

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print(user_form.errors, profile_form.errors)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = GuideProfileForm()

    # Render the template depending on the context.
    return render(request,
                  "registration/guide-login.html",
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def traveler_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        user_form = UserForm()
        profile_form = TravelerProfileForm()
        return render(request, 'registration/login.html',
                      {'user_form': user_form, 'profile_form': profile_form})

def guide_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        user_form = UserForm()
        profile_form = GuideProfileForm()
        return render(request, 'registration/guide-login.html',
                      {'user_form': user_form, 'profile_form': profile_form})



@login_required
def user_logout(request):
    
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
