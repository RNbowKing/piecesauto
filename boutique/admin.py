from datetime import datetime
from django.contrib import admin
from boutique.models import ETAT_COMMANDE_CHOICES, Categorie, Commande, Constructeur, Modele, Produit, Reclamation, ProfilClient, MessageReclamation, ChangementEtatCommande, EntreeDeCommande
from django.db.models import Q


class ConstructeurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    search_fields = ('nom', 'slug')


class ModeleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'constructeur', 'nom', 'annee')
    fieldsets = [
        (None,               {'fields': ['nom', 'annee']}),
        ('Constructeur', {'fields': ['constructeur']}),
    ]
    list_filter = ('constructeur', 'annee',)
    search_fields = ('nom',)


class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    fields = ['nom', 'slug']
    search_fields = ('nom', 'slug')


class ProduitAdmin(admin.ModelAdmin):
    list_display = ('reference', 'nom', 'prix_ttc', 'stock', 'categorie')
    fieldsets = [
        ('Informations de base', {'fields': [
         'reference', 'nom', 'descriptif', 'categorie', 'modeles_compatibles']}),
        ('Tarification', {'fields': ['prix_ttc']}),
        ('Gérer le stock', {'fields': ['stock']}),
    ]
    list_filter = ('categorie', 'modeles_compatibles')
    search_fields = ('nom', 'reference')
    filter_horizontal = 'modeles_compatibles',


class EtatCommandeInline(admin.TabularInline):
    model = ChangementEtatCommande
    extra = 1
    fields = ('etat', 'date')
    readonly_fields = ('date',)

    def has_change_permission(self, request, obj):
        return False


class EntreeCommandeInline(admin.TabularInline):
    model = EntreeDeCommande
    extra = 2


@admin.action(description='Marquer les commandes sélectionnées comme expédiées et actualiser le stock')
def expedier_commande(modeladmin, request, queryset):
    for com in queryset:
        for ent in com.entreedecommande_set.all():
            prod = Produit.objects.get(id=ent.produit.id)
            prod.stock = prod.stock - ent.quantite
            prod.save()
        ch = ChangementEtatCommande(
            commande=com, etat='sen', date=datetime.now())
        ch.save()


class DernierEtatFilter(admin.SimpleListFilter):
    title = 'état actuel'
    parameter_name = 'dernier_etat'

    def lookups(self, request, model_admin):
        return ETAT_COMMANDE_CHOICES

    def queryset(self, request, queryset):
        if(not self.value()):
            return queryset
        ids = []
        for obj in queryset.filter(Q(changementetatcommande__etat=self.value())).distinct():
            if obj.dernier_code_etat() == self.value():
                ids.append(obj.id)
        return queryset.filter(id__in=ids)


class CommandeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'client', 'dernier_etat', 'dernier_etat_date')
    # fields = ['est_ouvert', 'commande']
    list_filter = ('client', DernierEtatFilter)
    inlines = [EtatCommandeInline, EntreeCommandeInline]
    actions = [expedier_commande]


class MessageReclamationInline(admin.TabularInline):
    model = MessageReclamation
    extra = 1
    fields = ('sujet', 'message', 'envoye_le', 'inward')
    readonly_fields = ('envoye_le',)

    def has_change_permission(self, request, obj):
        return False


@admin.action(description='Fermer les réclamations sélectionnées')
def fermer_reclamations(modeladmin, request, queryset):
    queryset.update(est_ouvert=False)


@admin.action(description='Marquer les réclamations sélectionnées comme lues')
def lire_reclamations(modeladmin, request, queryset):
    queryset.update(nouveaux_messages=False)


class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'commande', 'est_ouvert', 'nouveaux_messages',
                    'dernier_message', 'date_dernier_message')
    fields = ['est_ouvert', 'commande']
    list_filter = ('est_ouvert', 'commande', 'nouveaux_messages')
    inlines = [MessageReclamationInline]
    actions = [fermer_reclamations, lire_reclamations]


@admin.action(description='Effacer les données personnelles des profils sélectionnés')
def rendre_profil_anonyme(modeladmin, request, queryset):
    for com in queryset:
        com.nom_entreprise = ""
        com.adresse_ligne1 = ""
        com.adresse_ligne2 = ""
        com.code_postal = ""
        com.ville = ""
        com.telephone = ""
        com.user.first_name = "DeletedUser"
        com.user.last_name = str(datetime.now().timestamp()).replace('.', '')
        com.user.email = f"deleted{com.user.last_name}@example.com"
        com.user.is_active = False
        com.save()
        com.user.save()


class ProfilClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'nom_entreprise', 'adresse_ligne1',
                    'adresse_ligne2', 'code_postal', 'ville')
    fieldsets = [
        ('Compte utilisateur', {'fields': ['user']}),
        ('Informations client', {'fields': ['nom_entreprise', 'adresse_ligne1',
                                            'adresse_ligne2', 'code_postal', 'ville', 'telephone']}),
    ]
    list_filter = ('nom_entreprise', 'ville')
    search_fields = ('user__username', 'nom_entreprise', 'adresse_ligne1',
                     'adresse_ligne2', 'code_postal', 'ville', 'telephone'),
    actions = [rendre_profil_anonyme, ]


admin.site.register(Constructeur, ConstructeurAdmin)
admin.site.register(Modele, ModeleAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(Produit, ProduitAdmin)
admin.site.register(Commande, CommandeAdmin)
admin.site.register(Reclamation, ReclamationAdmin)
admin.site.register(ProfilClient, ProfilClientAdmin)
