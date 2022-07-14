from django.shortcuts import render
from django.views.decorators.cache import cache_page
from boutique.models import Constructeur, Modele, Categorie, Produit
from django.db.models.functions import Concat
from django.db.models import F, CharField
import json


@cache_page(604800)
def index(request):
    items = Constructeur.objects.all().annotate(
        item_slug=F('slug'), item_label=F('nom'))
    context = {
        'breadcrumb': [{'url': '/', 'title': 'Accueil', 'active': False}],
        'list_title': 'Votre constructeur',
        'list_description': 'Sélectionnez le constructeur de votre voiture.',
        'list_icons': 'bi-wrench-adjustable',
        'list_items': items,
        'slug_prefix': '/browse/'
    }
    return render(request, 'catalogue/list.html', context)


@cache_page(604800)
def browse_constructeur(request, constructeur_slug):
    constructeur = Constructeur.objects.get(slug=constructeur_slug)
    items = Modele.objects.filter(constructeur__id=constructeur.id).order_by('nom').annotate(
        item_slug=F('id'), item_label=Concat('nom', 'annee', output_field=CharField()))
    context = {
        'breadcrumb': [
            {'url': '/browse/', 'title': 'Accueil', 'active': True},
            {'url': f'/browse/{constructeur.slug}',
                'title': constructeur.nom, 'active': False}
        ],
        'list_title': f'Votre modèle de véhicule {constructeur.nom}',
        'list_description': 'Sélectionnez le modèle de véhicule pour lequel vous recherchez des pièces.',
        'list_icons': 'bi-truck',
        'list_items': items
    }
    return render(request, 'catalogue/list.html', context)


@cache_page(604800)
def browse_modele(request, constructeur_slug, modele_id):
    constructeur = Constructeur.objects.get(slug=constructeur_slug)
    modele = Modele.objects.get(id=modele_id)
    items = Categorie.objects.all().order_by('nom').annotate(
        item_slug=F('slug'), item_label=F('nom'))
    context = {
        'breadcrumb': [
            {'url': '/browse/', 'title': 'Accueil', 'active': True},
            {'url': f'/browse/{constructeur.slug}',
                'title': constructeur.nom, 'active': True},
            {'url': f'/browse/{constructeur.slug}/{modele.id}',
             'title': f'{modele.nom} ({modele.annee})', 'active': False}
        ],
        'list_title': 'Catégories',
        'list_description': 'Cherchez votre produit parmi les catégories de notre catalogue.',
        'list_icons': 'bi-boxes',
        'list_items': items
    }
    return render(request, 'catalogue/list.html', context)


@cache_page(604800)
def browse_categorie(request, constructeur_slug, modele_id, categorie_slug):
    constructeur = Constructeur.objects.get(slug=constructeur_slug)
    modele = Modele.objects.get(id=modele_id)
    categorie = Categorie.objects.get(slug=categorie_slug)
    items = Produit.objects.filter(categorie__id=categorie.id, modeles_compatibles__in=[modele]).order_by('nom').annotate(
        item_slug=F('id'), item_label=F('nom'), item_description=F('descriptif'), item_price=F('prix_ttc'))
    context = {
        'breadcrumb': [
            {'url': '/browse/', 'title': 'Accueil', 'active': True},
            {'url': f'/browse/{constructeur.slug}',
                'title': constructeur.nom, 'active': True},
            {'url': f'/browse/{constructeur.slug}/{modele.id}',
             'title': f'{modele.nom} ({modele.annee})', 'active': True},
            {'url': f'/browse/{constructeur.slug}/{modele.id}/{categorie_slug}',
             'title': categorie.nom, 'active': False}
        ],
        'list_title': f'Produits {categorie.nom} compatibles avec {modele.nom} ({modele.annee})',
        'list_description': 'Cherchez votre produit.',
        'list_icons': 'bi-box',
        'list_items': items,
        'slug_prefix': '/catalogue/'
    }
    return render(request, 'catalogue/cards_list.html', context)


@cache_page(60)
def view_product(request, product_id, msg=''):
    product = Produit.objects.get(id=product_id)
    if product.stock == 0:
        msg = 'Ce produit est indisponible pour le moment.'

    context = {
        'breadcrumb': [
            {'url': '/catalogue/', 'title': 'Catalogue', 'active': True},
            {'url': f'/catalogue/',
             'title': product.categorie, 'active': False},
            {'url': f'/catalogue/{product_id}',
             'title': product.reference, 'active': False}
        ],
        'product': product,
        'modeles_compatibles': product.modeles_compatibles.all(),
        'msg': msg
    }

    return render(request, 'catalogue/product_view.html', context)


def add_to_panier(request, product_id):
    product = Produit.objects.get(id=product_id)
    qte = int(request.POST['qte'])
    previous_qte = 0
    new_qte = qte
    if 'mespiecesauto.panier' in request.COOKIES:
        panier = json.loads(request.COOKIES['mespiecesauto.panier'])
        if str(product_id) in panier:
            previous_qte = panier[str(product_id)]
            new_qte = previous_qte + qte
            panier[str(product_id)] = new_qte
        else:
            panier[str(product_id)] = qte
    else:
        panier = {str(product_id): qte}

    if new_qte > product.stock:
        return view_product(request, product_id, f'Vous ne pouvez commander cette pièce que dans la limite du stock disponible. Il y en a déjà {previous_qte} dans votre panier.')

    response = view_product(request, product_id,
                            'Ajouté au panier avec succès.')
    response.set_cookie('mespiecesauto.panier', json.dumps(
        obj=panier, ensure_ascii=True), max_age=604800)
    return response
