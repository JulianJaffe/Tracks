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
        #perhaps need to log in the user as well?
        #Need error handling
##        email = request.POST.get('email')
##        password = request.POST.get('password')
##        firstName = request.POST.get('firstName')
##        lastName = request.POST.get('lastName')
##        confirm = request.POST.get('confirm')
        #user = TracksUser.objects.create_user(email, firstName, lastName, confirm, password)
        return HttpResponseRedirect('/Tracks/upload') #Should be changed to user's profile?
    else:
        form = TracksUserCreationForm()
    return render(request, 'Tracks/signup.html', {'form': form})

    
def signIn(request):
    # Custom login
    email = password = msg = ''
    if request.POST:
        form = TracksUserSignInForm(request.POST)
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = authenticate(username=email, password=password) #Unlike the TracksUserCreationForm, this form does not do the required work
        #Need error handling
        if user is not None:
            if user.is_active:
                login(request, user)
            else:
                #Will we ever have inactive users? Maybe instead of deletion?
                #msg = 'That user is inactive!' (does this reveal too much information about a user?)
                #render(request, 'Tracks/signin.html', {'form': form, 'msg': msg})
                pass
        else:
            #Invalid password, we need to alert the user
            #msg = 'Invalid username/password combination!'
            #render(request, 'Tracks/signin.html', {'form': form, 'msg': msg})
            pass
        #if next in request.POST:
            #We've been redirected; return the user where they want to go
            #url = request.POST.get('next')
            #HttpResponseRedirect(url)
        return HttpResponseRedirect('') # should be user's profile when ready
    else:
        form = TracksUserSignInForm()
    return render(request, 'Tracks/signin.html', {'form': form})

def logout(request):
    logout(request)
    return HttpResponseRedirect('') #should be a log out page instead

def tracks(request):
    return render(request, 'Tracks/tracks.html',{})

def about(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/about.html', {})

#@login_required
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
