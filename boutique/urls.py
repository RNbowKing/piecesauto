from django.urls import path

from boutique.views import catalogue, espaceclient, authentication, commande

urlpatterns = [
    path('', catalogue.index, name='index'),
    path('browse/', catalogue.index, name='index'),
    path('browse/<str:constructeur_slug>/', catalogue.browse_constructeur, name='browse_constructeur'),
    path('browse/<str:constructeur_slug>/<int:modele_id>/', catalogue.browse_modele, name='browse_modele'),
    path('browse/<str:constructeur_slug>/<int:modele_id>/<str:categorie_slug>/', catalogue.browse_categorie, name='browse_categorie'),
    path('catalogue/', catalogue.index, name='index'),
    path('catalogue/<int:product_id>/', catalogue.view_product, name='view_product'),
    path('catalogue/<int:product_id>/ajouter', catalogue.add_to_panier, name='add_to_panier'),

    path('auth/logout', authentication.logout_view, name='logout_view'),
    path('auth/login', authentication.login_form, name='login_form'),
    path('auth/submitlogin', authentication.login_submit, name='login_submit'),
    path('auth/newaccount', authentication.newaccount_form, name='newaccount_form'),
    path('auth/submitnewaccount', authentication.newaccount_submit, name='newaccount_submit'),

    path('espaceclient/', espaceclient.index, name='espaceclient_index'),
    path('espaceclient/panier/', espaceclient.view_panier, name='view_panier'),
    path('espaceclient/panier/vider', espaceclient.vider_panier, name='vider_panier'),
    path('espaceclient/panier/changer', espaceclient.changer_panier, name='changer_panier'),
    path('espaceclient/compte/', espaceclient.compte_form, name='compte_form'),
    path('espaceclient/compte/change', espaceclient.compte_submit, name='compte_submit'),
    path('espaceclient/profil/', espaceclient.profil_form, name='profil_form'),
    path('espaceclient/profil/change', espaceclient.profil_submit, name='profil_submit'),
    path('espaceclient/commandes/', espaceclient.view_commandes, name='view_commandes'),
    path('espaceclient/commandes/<int:commande_id>/', espaceclient.view_commande_historique, name='view_commande_historique'),
    path('espaceclient/commandes/<int:commande_id>/reclamation/', espaceclient.view_commande_reclamation, name='espaceclient.view_commande_reclamation'),
    path('espaceclient/commandes/<int:commande_id>/reclamation/new', espaceclient.new_reclamation, name='espaceclient.new_reclamation'),
    path('espaceclient/commandes/<int:commande_id>/reclamation/sendmessage', espaceclient.new_reclamation_message, name='espaceclient.new_reclamation_message'),

    path('commande/saisie', commande.saisie_form, name='saisie_form'),
    path('commande/paiement', commande.paiement_form, name='paiement_form'),
    path('commande/recap', commande.recap_view, name='recap_view'),
]