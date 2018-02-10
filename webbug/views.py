from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Bug, Hit
from django.contrib.auth.models import User
from pprint import pprint as pp
from pprint import pformat
import json, uuid, os
from . import settings

@csrf_protect
def home(request):
    if request.user.is_authenticated:
        return user_index(request)

    return render(request, 'login.html')

@login_required
def user_index(request):
    bugs = Bug.objects.filter(owner=request.user)
    return render(request, 'index.html', {'bugs':bugs})


@csrf_protect
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
    return redirect('/')

@login_required
def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def hits(request, webbug_id):
    bug = Bug.objects.filter(id=webbug_id).first()
    if not bug or not bug.owner == request.user:
        return HttpResponseForbidden()
    _hits = Hit.objects.filter(bug=bug).order_by('-date')
    return render(request, 'bug_details.html', {'webbug': bug, 'hits': _hits})

@login_required
def create_sniper(request):
    owner = request.user
    Bug(owner=owner).save()
    return redirect('/')


# @csrf_protect
# @login_required
# def new_sniper(request):
#     return render(request, 'new_sniper.html')

@login_required
def user_profile(request):
    return render(request, 'profile.html')

def new_account(request):
    return render(request, 'new_user.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username,password=password).save()
    return redirect('/')



def serve_bug(request, webbug_id):
    bug = Bug.objects.filter(id=webbug_id).first()
    if bug:
        dumpable_meta = {x: y for x, y in request.META.iteritems() if isinstance(y,str)}
        new_hit = Hit(bug=bug,
                      http_headers_json=json.dumps(dumpable_meta),
                      cookies_json=json.dumps(request.COOKIES))
        if 'HTTP_REFERER' in request.META:
            new_hit.http_referer = request.META['HTTP_REFERER']
        if 'REMOTE_ADDR' in request.META:
            new_hit.remote_addr = request.META['REMOTE_ADDR']
        if 'REMOTE_PORT' in request.META:
            new_hit.remote_port = request.META['REMOTE_PORT']
        if 'HTTP_X_REAL_IP' in request.META:
            new_hit.real_ip = request.META['HTTP_X_REAL_IP']
        new_hit.save()

        #image_data = open(os.path.join(settings.BASE_DIR,"static/a.png"), "rb").read()
        #white pixel
        image_data = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00$\xe8\x00\x00$\xe8\x01\x82c\x05\x1c\x00\x00\x00\rIDAT\x18Wc\xf8\xff\xff\xff\x7f\x00\t\xfb\x03\xfd\x05CE\xca\x00\x00\x00\x00IEND\xaeB`\x82'
        resp = HttpResponse(image_data, content_type="image/png")
        resp['Cache-Control'] = 'no-cache, no-store'

        if 'i' in request.COOKIES:
            resp.set_cookie('i', str(int(request.COOKIES['i']) + 1))
        else:
            resp.set_cookie('i', '1')

        if 'uuid' not in request.COOKIES:
            _uuid = str(uuid.uuid1())
            resp.set_cookie('uuid', _uuid)
            new_hit.uuid = _uuid
        else:
            new_hit.uuid = request.COOKIES['uuid']
        new_hit.save()

        return resp
    else:
        return HttpResponseForbidden()


@login_required
def hit_details(request, hit_id):
    hit = Hit.objects.filter(id=hit_id).first()
    if not hit or request.user != hit.bug.owner:
        return HttpResponseForbidden()
    cookies = json.loads(hit.cookies_json)
    headers = json.loads(hit.http_headers_json)
    return render(request, 'hit_details.html', {'hit':hit,'cookies':cookies, 'headers':headers})


@login_required
def about(request):
    return render(request, 'about.html')