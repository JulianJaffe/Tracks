# Create your views here.
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
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
import json

import Project.settings
from django.core.servers.basehttp import FileWrapper
##def index(request):
##    form = UploadFileForm()
##    return render(request, 'Tracks/index.html', {'form': form})


def register(request):
    """Register a user."""
    email = password = ''
    if request.method == 'POST':
        #form = TracksUserCreationForm(request.POST)
        #perhaps need to log in the user as well?
        #Need error handling
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        confirm = request.POST.get('confirm')
        user = TracksUser.objects.create_user(email, firstName, lastName, confirm, password)
        ## request.session['email'] = user.email
        return HttpResponseRedirect('/Tracks/userpage/')
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
                if next in request.POST:
                    #We've been redirected; return the user where they want to go
                    url = request.POST.get('next')
                    HttpResponseRedirect(url)
                request.session['email'] = user.email # NEW ADD WHICH IS BUGGY
                return HttpResponseRedirect('/Tracks/userpage') # should be user's profile when ready
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
    else:
        form = TracksUserSignInForm()
    return render(request, 'Tracks/signin.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/Tracks') #should be a log out page instead

def tracks(request):
    return render(request, 'Tracks/tracks.html',{})


def about(request):
    if (request.method == 'GET'):
        return render(request, 'Tracks/about.html', {})



@login_required
def userprofile(request, user_id=None):
    try:
        temp_user, is_disabled = TracksUser.get_user_desired_to_be_viewed(request, user_id)
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response

    if(TracksUser.has_userprofile(temp_user)):
        temp_instance = temp_user.userprofile
    else:
        temp_instance = UserProfile(user=temp_user)

    if(request.method == 'GET'):
        ##if(user_id == temp_user.email):
        form = UserProfileForm(instance=temp_instance)
        return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form, 'is_disabled' : is_disabled})
##        else:
##            form = UserProfileForm(readonly_form=True, instance=temp_instance)
##            return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})

    elif (request.method == 'POST'):
        form = UserProfileForm(request.POST, instance=temp_instance)
        if(form.is_valid()):
            try:
                form.save()
                return HttpResponseRedirect('/Tracks/userpage/');
            except:
                response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
                response.status_code = 500;
                return response
        else:
            form = UserProfileForm(instance=temp_instance)
            return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})

    else:
        response = HttpResponse('Fatal Error!')
        response.status_code = 500;
        return response



@login_required
def userpage(request, user_id=None):
    print (Project.settings.MEDIA_ROOT)
    try:
        temp_user, is_disabled = TracksUser.get_user_desired_to_be_viewed(request, user_id)
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response

    if(request.method == "GET"):
        form = UploadFileForm()
        ##return render(request, 'Tracks/index.html', {'form': form})
        list_of_tracks = temp_user.track_set.all() # need to pass this to a function first which checks if the filepaths are still accurate
        list_of_collaborations = temp_user.collaboration_set.all() ##[]
##        for track in list_of_tracks:
##            for temp_collaboration in track.collaboration_set.all():
##                if(list_of_collaborations.count(temp_collaboration) == 0):
##                    list_of_collaborations.append(temp_collaboration)

        return render(request, 'Tracks/userpage.html', {'user' : temp_user, 'form' : form, 'is_disabled' : is_disabled,
                                                            'list_of_tracks' : list_of_tracks, 'list_of_collaborations' : list_of_collaborations})





@login_required
def search(request):
    if(request.method == "GET"):
        searchString = request.GET.get('search', None)
        # TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this.
        filtered_query_set = search_relevant_models(searchString)
        return render(request, 'Tracks/search.html', {'filtered_query_set' : filtered_query_set})
    else:
        response = HttpResponse('you sent a GET request to search') # message string probably needs to change for production version
        response.status_code = 500;
        return response


@login_required
def downbeat(request):
    if (request.method == 'GET'):
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_user_desired_to_be_viewed(request, None)
        downbeat_list = History.get_downbeat_for(temp_user)
        return render(request, 'Tracks/downbeat.html', {'user' : temp_user, 'downbeat_list' : downbeat_list})


# Function for JSON Call
def get_tracks_for_current_user_JSON(request):
    try:
##        #temp_user = TracksUser.objects.get(email='test') #temporary line. FOR TESTING ONLY
##        temp_user = TracksUser.objects.get(email=request.session.get('email')) # NEW ADD WHICH IS
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_user_desired_to_be_viewed(request, None)
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response

    response_data = {}
    list_of_tracks = temp_user.track_set.all()
    for track in list_of_tracks:
        response_data[track.id] = track.filename

    response = HttpResponse(json.dumps(response_data), content_type="application/json")
    return response

# Function for AJAX Call
def finalize_collaboration(request):
    try:
        #track1_id = int(request.POST['track1_id'])
        #track2_id = int(request.POST['track2_id'])
        track1_id = int(request.POST.get('track1_id', 0))
        track2_id = int(request.POST.get('track2_id', 0))
        collab_id = int(request.POST.get('collab_id', 0))
        mod_type = request.POST['mod_type']

        collab = Collaboration.handle_finalization(track1_id, track2_id, collab_id, mod_type)
##        track1 = Track.objects.get(id=track1_id)
##        track2 = Track.objects.get(id=track2_id)
##
##        temp_collab = Collaboration()
##        temp_collab.save()
##
##        temp_collab.tracks.add(track1)
##        temp_collab.tracks.add(track2)
##        temp_collab.users.add(track1.user)
##        temp_collab.users.add(track2.user)
##
##        if(track1.user != track2.user):
##            History.add_history(track1.user, temp_collab, ADDED_HISTORY)
##            History.add_history(track2.user, temp_collab, ADDED_HISTORY)
##        else:
##            History.add_history(track1.user, temp_collab, ADDED_HISTORY)


        response = HttpResponse('track1_id = ' + str(track1_id) + 'track2_id = ' + str(track2_id) + 'collab_id = ' + str(collab.id))
        response.status_code = 200;
        return response
    except:
        response = HttpResponse(traceback.format_exc()) # Currently sends a response with the traceback of the error. DO NOT USE IN PRODUCTION.
        response.status_code = 500;
        return response


# Fuction for AJAX Call

def upload_MP3(request):
    #currently the size of the file is a static final, however we should consider having a quota per user, in case a user wishes to extend their quota.
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 52428800
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160
    SIZE_LIMIT = 5242880
    #print('entered uploadmp3')
    #list of acceptable extensions. make sure it starts with a dot'
    acceptableFormats = ['.mp3']
    if (request.method == 'POST'):
        form = UploadFileForm(request.POST, request.FILES)
        if (form.is_valid()):
            try:
                temp_mp3 = request.FILES['file']
                #check the size of the file
                sizeOfFile = temp_mp3._size
                notSupported = True
                for name in acceptableFormats:
                    if temp_mp3.name.endswith(name):
                       notSupported = False
                if notSupported:
                    response = HttpResponse('File extension not supported')
                    response.status_code = 500;
                    return response

                if sizeOfFile > SIZE_LIMIT:
                    response = HttpResponse('File exceeding size limit')
                    response.status_code = 500;
                    return response

##                temp_user = TracksUser.objects.get(email=request.POST['user_email'])
                # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
                temp_user, is_disabled = TracksUser.get_user_desired_to_be_viewed(request, None)

                new_track = Track(user = temp_user, filename=temp_mp3.name)
                new_track.handle_upload_file(temp_mp3)
                History.add_history(new_track.user, new_track, ADDED_HISTORY)

                response_data = {"server_filename" : new_track.get_server_filename(), "track_id" : new_track.id}
                response = HttpResponse(json.dumps(response_data), content_type="application/json") #HttpResponse('success')
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





def play_MP3(request, path):
    filepath = os.path.join(Project.settings.MEDIA_ROOT, path).replace('\\', '/')
    #print(filepath)
    wrapper = FileWrapper(open(filepath, 'rb'))
    response = StreamingHttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'attachment; filename=%s' % path
    return response

