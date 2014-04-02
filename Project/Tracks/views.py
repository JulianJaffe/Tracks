# Create your views here.
from django import forms
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import *
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
## from TracksApp_forms import *
from Tracks.forms import *
##from Tracks.forms import UploadFileForm
from Tracks.models import *
##from Tracks.models import TracksUser
##from Tracks.models import Track
from models import *
import os
##import sys
import traceback
import json

# need these for serving mp3 files from this Django server. If another server handles serving mp3 files, these can be removed.
# see play_mp3 function at bottom of page for more details.
import Project.settings
from django.core.servers.basehttp import FileWrapper

"""
TODO:
    - (in userpage.html) allow removal of tracks.

    - (in nav bar) upload in top nav bar goes to userpage. need to add functionality to nav bar upload so that an upload dialog opens.
         also need a nav bar option to go to userpage (and maybe userprofile page).

    - (in nav bar) need link in nav bar to register.

    - (in nav bar) need link in nav bar to sign in.

    - (in userpage.html) need to change the class of collabs which finished playing from "play" to "pause" (and seek audio to 0).

"""


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
        set_session_for_user(request, user)
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
                ##request.session['email'] = user.email # NEW ADD WHICH IS BUGGY
                set_session_for_user(request, user)
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
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), user_id)
##    if(TracksUser.has_userprofile(temp_user)):
##        temp_instance = temp_user.userprofile
##    else:
##        temp_instance = UserProfile(user=temp_user)

        temp_instance = temp_user.get_user_profile()

        if(request.method == 'GET'):
            form = UserProfileForm(instance=temp_instance)
            return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form, 'is_disabled' : is_disabled})

        elif (request.method == 'POST'):
            form = UserProfileForm(request.POST, instance=temp_instance)
            if(form.is_valid()):
                try:
                    form.save()
                    return HttpResponseRedirect('/Tracks/userpage/');
                except:
                    response = HttpResponse('userprofile could not be saved') # May need to change message sent
                    print(traceback.format_exc()) # for debugging purposes only. DO NOT USE IN PRODUCTION
                    response.status_code = 500;
                    return response
            else:
                form = UserProfileForm(instance=temp_instance)
                return render(request, 'Tracks/userprofile.html', {'user' : temp_user, 'form' : form})

        else:
            response = HttpResponse('Request was neither a GET or a POST') # Probably a good idea to mark as DO NO USE IN PRODUCTION.
            response.status_code = 500;
            return response

    except:
        response = HttpResponse('error in userprofile') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response



@login_required
def userpage(request, user_id=None):
    try:
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), user_id)

        if(request.method == "GET"):
            form = UploadFileForm()
            list_of_tracks = temp_user.get_tracks_list()
            list_of_collaborations = temp_user.get_collaborations_list()
            return render(request, 'Tracks/userpage.html', {'user' : temp_user, 'form' : form, 'is_disabled' : is_disabled,
                                                                'list_of_tracks' : list_of_tracks, 'list_of_collaborations' : list_of_collaborations})

    except:
        response = HttpResponse('error in userpage') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response





@login_required
def search(request):
    if(request.method == "GET"):
        searchString = request.GET.get('search', None)
        # TODO: for security purposes, need to make sure that searchString does not contain any malicious code. Check to see if Django provides some help for this.
        filtered_query_set = search_relevant_models(searchString)
        return render(request, 'Tracks/search.html', {'filtered_query_set' : filtered_query_set})
    else:
        response = HttpResponse('you did not send a GET request to search') # message string probably needs to change for production version
        response.status_code = 500;
        return response


@login_required
def downbeat(request):
    if (request.method == 'GET'):
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)
        downbeat_list = History.get_downbeat_for(temp_user)
        return render(request, 'Tracks/downbeat.html', {'user' : temp_user, 'downbeat_list' : downbeat_list})


# Function for JSON Call
def get_tracks_for_current_user_JSON(request):
    try:
        # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)

##    response_data = {}
##    list_of_tracks = temp_user.track_set.all()
##    for track in list_of_tracks:
##        response_data[track.id] = track.filename

        response_data = temp_user.get_tracks_list_JSON()

        response = HttpResponse(json.dumps(response_data), content_type="application/json")
        return response
    except:
        response = HttpResponse('error trying to send list of tracks for current user') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response

# Function for AJAX Call
def finalize_collaboration(request):
    try:
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

        response = HttpResponse('success') ## render(request, 'Tracks/collaboration_for_AJAX.html', {'collaboration' : collab})
        response.status_code = 200;
        return response
    except:
        response = HttpResponse('error trying to finalize collaboration') # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response


# Fuction for AJAX Call

def upload_MP3(request):
##    #currently the size of the file is a static final, however we should consider having a quota per user, in case a user wishes to extend their quota.
##    # 2.5MB - 2621440
##    # 5MB - 5242880
##    # 10MB - 10485760
##    # 20MB - 20971520
##    # 50MB - 52428800
##    # 100MB 104857600
##    # 250MB - 214958080
##    # 500MB - 429916160
##    SIZE_LIMIT = 5242880
##    #print('entered uploadmp3')
##    #list of acceptable extensions. make sure it starts with a dot'
##    acceptableFormats = ['.mp3']
    try:
        if (request.method == 'POST'):
            form = UploadFileForm(request.POST, request.FILES)
            if (form.is_valid()):

                    temp_file = request.FILES['file']
    ##                #check the size of the file
    ##                sizeOfFile = temp_file._size
    ##                notSupported = True
    ##                for name in acceptableFormats:
    ##                    if temp_file.name.endswith(name):
    ##                       notSupported = False
    ##                if notSupported:
    ##                    response = HttpResponse('File extension not supported')
    ##                    response.status_code = 500;
    ##                    return response
    ##
    ##                if sizeOfFile > SIZE_LIMIT:
    ##                    response = HttpResponse('File exceeding size limit')
    ##                    response.status_code = 500;
    ##                    return response

    ##                temp_user = TracksUser.objects.get(email=request.POST['user_email'])
                    # don't actually need the value of is_disabled, but getting it anyway as it is returned by the function
                    temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)

    ##                new_track = Track(user = temp_user, filename=temp_file.name)
    ##                new_track.handle_upload_file(temp_file)
    ##                History.add_history(new_track.user, new_track, ADDED_HISTORY)

                    server_filename, track_id, error = Track.handle_music_file_upload(temp_user, temp_file)

                    if(error != None):
                        response = HttpResponse(error)
                        response.status_code = 400;
                        return response

                    response_data = {"server_filename" : server_filename, "track_id" : track_id}
                    response = HttpResponse(json.dumps(response_data), content_type="application/json")
                    response.status_code = 200;
                    return response
            else:
                response = HttpResponse('form not valid')
                response.status_code = 400;
                return response
        else:
            response = HttpResponse('method not post')
            response.status_code = 400;
            return response

    except:
        response = HttpResponse('error with userprofile')  # May need to change message sent
        print(traceback.format_exc())  # for debugging purposes only. DO NOT USE IN PRODUCTION
        response.status_code = 500;
        return response



# Helper function for getting session. SHOULD NOT BE REQUESTED BY THE CLIENT
def get_session_for_user(request):
    return request.session['email']

# Helper function for setting session. SHOULD NOT BE REQUESTED BY THE CLIENT
def set_session_for_user(request, temp_user):
    request.session['email'] = temp_user.email
    request.session.set_expiry(1800) # set expiration to 30 min


# Allows the server to serve audio/mpeg files (e.g. mp3 files). Can be removed if another server is responsible for serving audio/mpeg files.
def play_MP3(request, path):
    filepath = os.path.join(Project.settings.MEDIA_ROOT, path).replace('\\', '/')
    #print(filepath)
    wrapper = FileWrapper(open(filepath, 'rb'))
    response = StreamingHttpResponse(wrapper, content_type='audio/mpeg')
    response['Content-Length'] = os.path.getsize(filepath)
    response['Content-Disposition'] = 'attachment; filename=%s' % path
    return response

@login_required
@ensure_csrf_cookie
def record(request):
    #get user
    user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)
    if not is_disabled:
        return render(request, 'Tracks/record.html', {'user': user})
    else:
        return render(request, 'Tracks/disabled')

@login_required
def handleRecord(request):
    """
    Saves a user-recorded blob as an .mp3.
    """
    if not request.method == 'POST' or not request.is_ajax():
        raise Http404
    file_name = request.POST.get('filename')
    audio = request.FILES.get('audio')
    SIZE_LIMIT = 5242880 #Should probably be made global, currently same as upload_mp3's SIZE_LIMIT
    try:
        if audio.size > SIZE_LIMIT:
            #handle size error
            pass
        #need to convert from WAV to MP3
        temp_user, is_disabled = TracksUser.get_desired_user(get_session_for_user(request), None)
        new_track = Track(user=temp_user, filename=file_name)
        new_track.handle_upload_file(audio)
        History.add_history(new_track.user, new_track, ADDED_HISTORY)
        response = HttpResponse('success')
        response.status_code = 200;
        return response
    except:
        #handle error
        pass


