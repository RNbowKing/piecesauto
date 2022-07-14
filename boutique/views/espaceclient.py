from django.shortcuts import render, redirect
from boutique.models import ChangementEtatCommande, Commande, EntreeDeCommande, MessageReclamation, Produit, ProfilClient, Reclamation
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


def index(request):
    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': False},
        ],
        'is_authenticated': request.user.is_authenticated,
        'user': request.user
    }
    return render(request, 'espaceclient/index.html', context)


def view_panier(request, msg='', overwrite_panier=False, new_panier={}):
    if overwrite_panier:
        rawpanier = new_panier
    elif 'mespiecesauto.panier' in request.COOKIES:
        rawpanier = json.loads(request.COOKIES['mespiecesauto.panier'])
    else:
        rawpanier = {}

    if not rawpanier:
        msg = 'Votre panier est vide. Consultez le catalogue pour commencer vos achats !'
    panier = []
    for key, item in rawpanier.items():
        produit = Produit.objects.get(id=key)
        panier.append({'produit': produit, 'qte': item})

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/panier', 'title': 'Panier', 'active': False}
        ],
        'panier': panier,
        'msg': msg
    }
    return render(request, 'espaceclient/panier.html', context)


def vider_panier(request):
    response = view_panier(request, 'Panier vidé.', True)
    response.set_cookie('mespiecesauto.panier', json.dumps(
        obj={}, ensure_ascii=True), max_age=604800)
    return response


def changer_panier(request):
    product_id = request.POST['produit_id']
    new_qte = request.POST['new_qte']

    panier = json.loads(request.COOKIES['mespiecesauto.panier'])
    panier[str(product_id)] = new_qte

    response = view_panier(request, 'Panier modifié.', True, panier)
    response.set_cookie('mespiecesauto.panier', json.dumps(
        obj=panier, ensure_ascii=True), max_age=604800)
    return response


@login_required
def compte_form(request, msg=''):
    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/compte', 'title': 'Mon compte', 'active': False}
        ],
        'user': request.user,
        'msg': msg
    }
    return render(request, 'espaceclient/compte.html', context)


@login_required
def compte_submit(request, msg=''):
    password = request.POST['password']
    user = authenticate(
        request, username=request.user.username, password=password)

    if user is not None:
        user.email = request.POST['email']
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.save()
        msg = 'Effectué avec succès.'
    else:
        msg = 'Mot de passe incorrect.'

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/compte', 'title': 'Mon compte', 'active': False}
        ],
        'user': user,
        'msg': msg
    }
    return render(request, 'espaceclient/compte.html', context)


@login_required
def profil_form(request, msg=''):
    try:
        profil = ProfilClient.objects.get(user=request.user)
    except:
        profil = ProfilClient.objects.create(user=request.user)

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/profil', 'title': 'Mon profil', 'active': False}
        ],
        'profil': profil,
        'msg': msg
    }
    return render(request, 'espaceclient/profil.html', context)


@login_required
def profil_submit(request, msg=''):
    profil = ProfilClient.objects.get(user=request.user)

    profil.nom_entreprise = request.POST['nom_entreprise']
    profil.adresse_ligne1 = request.POST['adresse_ligne1']
    profil.adresse_ligne2 = request.POST['adresse_ligne2']
    profil.code_postal = request.POST['code_postal']
    profil.ville = request.POST['ville']
    profil.telephone = request.POST['telephone']
    profil.save()

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/profil', 'title': 'Mon profil', 'active': False}
        ],
        'profil': profil,
        'msg': 'Effectué avec succès.'
    }
    return render(request, 'espaceclient/profil.html', context)


@login_required
def view_commandes(request, msg=''):
    try:
        profil = ProfilClient.objects.get(user=request.user)
    except:
        profil = ProfilClient.objects.create(user=request.user)
    commandes = Commande.objects.filter(client=profil).order_by('-id')

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/commandes',
                'title': 'Mes commandes', 'active': False}
        ],
        'commandes': commandes,
        'msg': msg
    }
    return render(request, 'espaceclient/commandes.html', context)


@login_required
def view_commande_historique(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    entrees = EntreeDeCommande.objects.filter(commande__id=commande_id)
    totalpanier = 0
    for item in entrees:
        totalpanier += item.produit.prix_ttc*item.quantite
        item.total = item.produit.prix_ttc*item.quantite
    etats = ChangementEtatCommande.objects.filter(commande__id=commande_id).order_by('-date')

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/commandes',
                'title': 'Mes commandes', 'active': True},
            {'url': f'/espaceclient/commandes/{commande_id}', 'title': f'Commande #{commande_id}', 'active': False}
        ],
        'commande': commande,
        'entrees': entrees,
        'totalpanier': totalpanier,
        'etats': etats
    }
    return render(request, 'espaceclient/commande_historique.html', context)

@login_required
def view_commande_reclamation(request, commande_id):
    commande = Commande.objects.get(id=commande_id)

    try:
        reclamation = Reclamation.objects.filter(commande__id=commande_id).last()
        messages = MessageReclamation.objects.filter(reclamation=reclamation).order_by('envoye_le')
    except:
        messages = None
        reclamation = None

    context = {
        'breadcrumb': [
            {'url': '/espaceclient/', 'title': 'Espace client', 'active': True},
            {'url': '/espaceclient/commandes',
                'title': 'Mes commandes', 'active': True},
            {'url': f'/espaceclient/commandes/{commande_id}', 'title': f'Commande #{commande_id}', 'active': True},
            {'url': f'/espaceclient/commandes/{commande_id}/reclamation', 'title': f'Réclamation', 'active': False}
        ],
        'commande': commande,
        'reclamation': reclamation,
        'messages': messages
    }
    return render(request, 'espaceclient/reclamations.html', context)


@login_required
def new_reclamation(request, commande_id):
    commande = Commande.objects.get(id=commande_id)
    Reclamation.objects.create(commande=commande, est_ouvert=True)
    return redirect(f'/espaceclient/commandes/{commande_id}/reclamation/')


@login_required
def new_reclamation_message(request, commande_id):
    reclamation_id = request.POST['reclamation_id']
    reclamation = Reclamation.objects.get(id=reclamation_id)
    sujet = request.POST['sujet']
    message = request.POST['message']
    MessageReclamation.objects.create(reclamation=reclamation, sujet=sujet, message=message, inward=True)
    return redirect(f'/espaceclient/commandes/{commande_id}/reclamation/')
