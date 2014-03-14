# Create your views here.
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponseForbidden, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.utils import timezone
# from TracksApp_forms import *
from Tracks.forms import *
from Tracks.forms import UploadFileForm
from Tracks.models import *
from Tracks.models import TracksUser
from Tracks.models import Track
import os
import sys
import traceback


def index(request):
    form = UploadFileForm()
    return render(request, 'Tracks/index.html', {'form': form})


def register(request):
    """Register a user."""
    email = password = ''
    if request.method == 'POST':
        form = TracksUserCreationForm(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        confirm = request.POST.get('confirm')
        #user = TracksUser.objects.create_user(email, firstName, lastName, confirm, password)
        return render(request, 'Tracks/index.html', {'form': form})
    else:
        form = TracksUserCreationForm()
    return render(request, 'Tracks/signup.html', {'form': form})

    
 # Julian's version, undo when ready
def signIn(request):
    # Custom login
    email = password = ''
    print request
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('')

    return render_to_response('login.html', {'email': email})

def tracks(request):
    return render(request, 'Tracks/tracks.html',{})


##def signIn(request):
##    if (request.method == 'GET'):
##        return render(request, 'Tracks/welcome.html',{})


def about(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/about.html', {})


def upload_MP3(request):
    #print('entered uploadmp3')
    if (request.method == 'POST'):
        form = UploadFileForm(request.POST, request.FILES)
        if (form.is_valid):
            try:
                temp_mp3 = request.FILES['file']
                new_track = Track(filename=temp_mp3.name)
                handle_upload_file(temp_mp3, new_track)
                response = HttpResponse('success')
                response.status_code = 200;
                return response
            except:
                response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
                response.status_code = 500;
                return response
        else:
            response = HttpResponse('form not valid')
            response.status_code = 400;
            return response
    else:
        response = HttpResponse('method not post')
        response.status_code = 400;
        return response
