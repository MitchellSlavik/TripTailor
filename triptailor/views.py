from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Trip, Guide
from .forms import UserForm, TravelerProfileForm
from django.db.models import Q
# Create your views here.


def home(request):
    data = {
        "userLoggedIn": False,
        "searchResults": Trip.objects.all()
    }
    return render(request, "triptailor/home.html", data)


def searchTrip(request):
    if request.method == 'GET':
        searchcriteria = request.GET.get('search_criteria')
        startrange = request.GET.get('start_range')
        endrange = request.GET.get('end_range')
        try:
            data = {
                "searchResults": Trip.objects.filter(name__icontains=searchcriteria) |
                Trip.objects.filter(maxNumTravelers__icontains=searchcriteria) |
                Trip.objects.filter(description__icontains=searchcriteria) |
                Trip.objects.filter(cost__icontains=searchcriteria)
                #Trip.objects.filter(date__range=[startrange, endrange])
            }
        except Trip.DoesNotExist:
            data = {"searchResults": None}
        return render(request, "triptailor/search-results.html", data)
    else:
        return render(request, "home.html", {})


@login_required
def profile(request):
    data = {
        'hello': "hello colin"
    }
    return render(request, "registration/profile.html", data)


def trips(request):
    data = {
        'hello': "hello jonathan"
    }
    return render(request, "triptailor/trips.html", data)


def dashboard(request):
    data = {
        'hello': "hello carly"
    }
    return render(request, "triptailor/dashboard.html", data)


def createUserPage(request):
    data = {
        "userLoggedIn": False,
    }
    return render(request, "triptailor/create-user.html", data)


def createTrip(request):
    if request.user.is_authenticated:
        return render(request, "triptailor/create-trip.html", {})
    else:
        return(request, "triptailor/home.html", {})


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
        return(request, "triptailor/home.html", {})


def traveler_register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
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

# Use the login_required() decorator to ensure only those logged in can access the view.


@login_required
def traveler_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
