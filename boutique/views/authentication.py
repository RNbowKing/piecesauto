from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.views.decorators.cache import cache_page

from boutique.models import ProfilClient


@cache_page(604800)
def login_form(request, msg=''):
    if request.user.is_authenticated:
        return redirect('/espaceclient/')

    context = {
        'breadcrumb': [
            {'url': '/auth/', 'title': 'Authentification', 'active': False},
            {'url': '/auth/login', 'title': 'Se connecter', 'active': False},
        ],
        'msg': msg
    }

    if 'next' in request.GET:
        context['next'] = request.GET['next']

    if 'next' in request.POST:
        context['next'] = request.POST['next']

    if 'username' in request.POST:
        context['username'] = request.POST['username']

    return render(request, 'authentication/login.html', context)


def login_submit(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('/espaceclient/')
    else:
        return login_form(request, 'Informations incorrectes.')


def logout_view(request):
    logout(request)

    return redirect('/espaceclient/')


@cache_page(604800)
def newaccount_form(request, msg=''):
    if request.user.is_authenticated:
        return redirect('/espaceclient/')

    context = {
        'breadcrumb': [
            {'url': '/auth/', 'title': 'Authentification', 'active': False},
            {'url': '/auth/newaccount', 'title': 'Nouveau compte', 'active': False},
        ],
        'msg': msg
    }

    if 'next' in request.GET:
        context['next'] = request.GET['next']

    if 'next' in request.POST:
        context['next'] = request.POST['next']

    return render(request, 'authentication/newaccount.html', context)


def newaccount_submit(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    user = User.objects.create_user(username, email, password)
    profil = ProfilClient.objects.create(user=user)
    profil.save()
    if user is not None:
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        login(request, user)
        if 'next' in request.POST:
            return redirect(request.POST['next'])

        return redirect('/espaceclient/')
    else:
        return newaccount_form(request, 'Informations incorrectes.')
