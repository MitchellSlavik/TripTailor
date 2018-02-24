from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User, AbstractUser, Group, Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import *

@permission_required('triptailor.is_guide')
def view_dashboard(request):
    data = {
        "trips": request.user.guide.trips.all()
    }

    return render(request, 'triptailor/dashboard.html', data)


@permission_required('triptailor.is_guide')
def create_trip(request):
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