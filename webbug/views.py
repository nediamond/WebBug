from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from models import CLSniper, Hit
from django.contrib.auth.models import User


@csrf_protect
def home(request):
    if request.user.is_authenticated:
        return user_index(request)

    return render(request, 'login.html')

@login_required
def user_index(request):
    snipers = CLSniper.objects.filter(owner=request.user)
    return render(request, 'index.html', {'snipers':snipers})


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
def hits(request, sniper_id):
    sniper = CLSniper.objects.filter(id=sniper_id).first()
    if not sniper or not sniper.owner == request.user:
        return HttpResponseForbidden()
    _hits = Hit.objects.filter(sniper=sniper).order_by('-date')
    return render(request, 'sniper_details.html', {'webbug': sniper, 'hits': _hits})

@login_required
def create_sniper(request):
    # TODO: Validate craigslist site
    owner = request.user
    site = request.POST['site']
    query = request.POST['query']
    # Needs better validation
    if site == '' or query == '':
        return redirect('/')
    min_price = request.POST['min_price'] or None
    max_price = request.POST['max_price'] or None
    search_titles = 'search_titles' in request.POST
    CLSniper(owner=owner,
             site=site, query=query,
             min_price=min_price,
             max_price=max_price,
             search_titles=search_titles).save()
    return redirect('/')


@csrf_protect
@login_required
def new_sniper(request):
    return render(request, 'new_sniper.html')

@login_required
def user_profile(request):
    return render(request, 'profile.html')

@login_required
def activate_sniper(request, sniper_id):
    sniper = CLSniper.objects.filter(id=sniper_id).first()
    if not sniper or not sniper.owner == request.user:
        return HttpResponseForbidden()
    sniper.active = True
    sniper.save()
    return redirect('/')

@login_required
def deactivate_sniper(request, sniper_id):
    sniper = CLSniper.objects.filter(id=sniper_id).first()
    if not sniper or not sniper.owner == request.user:
        return HttpResponseForbidden()
    sniper.active = False
    sniper.save()
    return redirect('/')

def new_account(request):
    return render(request, 'new_user.html')

def create_account(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(username=username,password=password).save()
    return redirect('/')
