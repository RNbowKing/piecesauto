from django.shortcuts import render, redirect
from boutique.models import ChangementEtatCommande, Commande, EntreeDeCommande, Produit, ProfilClient
from django.contrib.auth.decorators import login_required
import json


@login_required
def saisie_form(request):
    try:
        profil = ProfilClient.objects.get(user=request.user)
    except:
        return redirect('/espaceclient/profil')        

    if 'mespiecesauto.panier' in request.COOKIES:
        rawpanier = json.loads(request.COOKIES['mespiecesauto.panier'])
    else:
        return redirect('/espaceclient/panier')
    
    if not rawpanier: return redirect('/espaceclient/panier')  
    panier = []
    totalpanier = 0
    for key, item in rawpanier.items():
        produit = Produit.objects.get(id=key)
        panier.append({'produit': produit, 'qte': item, 'total': produit.prix_ttc*int(item)})
        totalpanier += produit.prix_ttc*int(item)
    
    context = {
        'user': request.user,
        'profil': profil,
        'panier': panier,
        'totalpanier': totalpanier
    }
    return render(request, 'commande/saisie.html', context)


@login_required
def paiement_form(request):
    try:
        profil = ProfilClient.objects.get(user=request.user)
    except:
        return redirect('/espaceclient/profil')   

    if 'mespiecesauto.panier' in request.COOKIES:
        rawpanier = json.loads(request.COOKIES['mespiecesauto.panier'])
    else:
        return redirect('/espaceclient/panier')  
    
    if not rawpanier: return redirect('/espaceclient/panier')  
    panier = []
    totalpanier = 0
    for key, item in rawpanier.items():
        produit = Produit.objects.get(id=key)
        panier.append({'produit': produit, 'qte': item, 'total': produit.prix_ttc*int(item)})
        totalpanier += produit.prix_ttc*int(item)
    
    context = {
        'user': request.user,
        'profil': profil,
        'panier': panier,
        'totalpanier': totalpanier
    }
    return render(request, 'commande/paiement.html', context)

@login_required
def recap_view(request):
    try:
        profil = ProfilClient.objects.get(user=request.user)
    except:
        return redirect('/espaceclient/profil')   

    if 'mespiecesauto.panier' in request.COOKIES:
        rawpanier = json.loads(request.COOKIES['mespiecesauto.panier'])
    else:
        return redirect('/espaceclient/panier')   
    
    if not rawpanier: return redirect('/espaceclient/panier')  
    panier = []
    totalpanier = 0
    commande = Commande.objects.create(
        client=profil
    )
    ChangementEtatCommande.objects.create(commande=commande,etat='new')
    for key, item in rawpanier.items():
        produit = Produit.objects.get(id=key)
        panier.append({'produit': produit, 'qte': item, 'total': produit.prix_ttc*int(item)})
        totalpanier += produit.prix_ttc*int(item)
        EntreeDeCommande.objects.create(commande=commande, produit=produit, quantite=item)
    
    context = {
        'user': request.user,
        'profil': profil,
        'panier': panier,
        'totalpanier': totalpanier
    }
    response = render(request, 'commande/recap.html', context)
    response.set_cookie('mespiecesauto.panier', json.dumps(
        obj={}, ensure_ascii=True), max_age=604800)
    return response