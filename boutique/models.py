from tabnanny import verbose
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib import admin


class Constructeur(models.Model):
    slug = models.CharField(max_length=200)
    nom = models.CharField(max_length=200)

    def __str__(self):
        return self.nom


class Modele(models.Model):
    nom = models.CharField(max_length=200)
    annee = models.IntegerField(verbose_name='année')
    constructeur = models.ForeignKey(
        to=Constructeur, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'modèle de véhicule'
        verbose_name_plural = 'modèles de véhicule'

    def __str__(self):
        return f"{self.constructeur.nom} {self.nom} ({self.annee})"


class Categorie(models.Model):
    slug = models.CharField(max_length=50, unique=True,
                            help_text='Indiquer une version simplifiée du nom de la catégorie, sans espace.')
    nom = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'catégorie'

    def __str__(self):
        return f"{self.nom} ({self.slug})"


class Produit(models.Model):
    reference = models.CharField(max_length=50, verbose_name='référence', help_text='Numéro ou code permettant d\'identifier votre produit')
    nom = models.CharField(max_length=255)
    descriptif = models.TextField(
        help_text='Donner une description aussi précise que possible')
    prix_ttc = models.DecimalField(
        decimal_places=2, max_digits=5, verbose_name='prix TTC')
    stock = models.IntegerField(
        help_text='Nombre de pièces actuellement en stock')
    categorie = models.ForeignKey(
        to=Categorie, on_delete=models.RESTRICT, verbose_name='Catégorie')
    modeles_compatibles = models.ManyToManyField(
        to=Modele, verbose_name='Modèles compatibles')

    def __str__(self):
        return f"{self.nom}"


class ProfilClient(models.Model):
    nom_entreprise = models.CharField(
        max_length=255, help_text='Raison sociale de l\'entreprise pour laquelle le client commande')
    adresse_ligne1 = models.CharField(
        max_length=255, help_text='Numéro, nom du bâtiment, nom de la rue.')
    adresse_ligne2 = models.CharField(
        max_length=255, help_text='Informations complémentaires', null=True, blank=True)
    code_postal = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    telephone = models.CharField(
        max_length=255, verbose_name='Numéro de téléphone')
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE, verbose_name='Compte utilisateur',
                                help_text='Indiquer ici le compte du client à qui lier les informations')

    class Meta:
        verbose_name = 'Profil de client'
        verbose_name_plural = 'Profils de clients'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} <{self.user}>"


ETAT_COMMANDE_CHOICES = [
    ('new', 'Nouvelle'),
    ('acc', 'Acceptée'),
    ('dec', 'Refusée'),
    ('sen', 'Expédiée'),
    ('dis', 'Livrée'),
    ('can', 'Annulée')
]


class Commande(models.Model):
    client = models.ForeignKey(
        to=ProfilClient, on_delete=models.RESTRICT, help_text='Client ayant passé la commande')

    def dernier_code_etat(self):
        return self.changementetatcommande_set.last().etat

    @admin.display(description='État actuel')
    def dernier_etat(self):
        return dict(ETAT_COMMANDE_CHOICES).get(self.changementetatcommande_set.latest().etat)

    @admin.display(description='Dernier changement le')
    def dernier_etat_date(self):
        return self.changementetatcommande_set.latest().date
    
    @admin.display(description='Éléments')
    def get_elements(self):
        return self.entreedecommande_set.all()
    
    @admin.display(description='Nombre d\'éléments')
    def get_nb_elements(self):
        return self.entreedecommande_set.count()

    def __str__(self):
        return f"Commande #{self.id}"


class EntreeDeCommande(models.Model):
    commande = models.ForeignKey(to=Commande, on_delete=models.RESTRICT)
    produit = models.ForeignKey(to=Produit, on_delete=models.RESTRICT)
    quantite = models.IntegerField(verbose_name='Quantité souhaitée')

    class Meta:
        verbose_name = 'ligne de commande'
        verbose_name_plural = 'lignes de commande'

    def __str__(self):
        return f"{self.produit} x{self.quantite} dans {self.commande}"


class ChangementEtatCommande(models.Model):
    commande = models.ForeignKey(to=Commande, on_delete=models.RESTRICT)
    etat = models.CharField(
        max_length=3, choices=ETAT_COMMANDE_CHOICES, verbose_name='état')
    date = models.DateTimeField(
        auto_now_add=True, help_text='Date à laquelle la commande a obtenu l\'état')
    
    @admin.display(description='État actuel')
    def etat_label(self):
        return dict(ETAT_COMMANDE_CHOICES).get(self.etat)

    class Meta:
        verbose_name = 'État de la commande'
        verbose_name_plural = 'États de la commande'
        get_latest_by='date'

    def __str__(self):
        return f"{self.commande} est devenue {self.etat} le {self.date}"


class Reclamation(models.Model):
    est_ouvert = models.BooleanField(
        default=True, verbose_name='ouverte', help_text='Une réclamation est considérée ouverte tant qu\'aucune issue n\'a été trouvée.')
    commande = models.ForeignKey(
        to=Commande, on_delete=models.RESTRICT, help_text='Commande concernée par la réclamation.')
    nouveaux_messages = models.BooleanField(default=True)

    class Meta:
        verbose_name='réclamation'

    def dernier_message(self):
        if (self.messagereclamation_set.exists()):
            return self.messagereclamation_set.last().sujet
        else:
            return ''

    def date_dernier_message(self):
        if (self.messagereclamation_set.exists()):
            return self.messagereclamation_set.last().envoye_le
        else:
            return ''

    def __str__(self):
        return f"Réclamation #{self.id}"


class MessageReclamation(models.Model):
    reclamation = models.ForeignKey(
        to=Reclamation, on_delete=models.RESTRICT)
    sujet = models.CharField(max_length=255)
    message = models.TextField()
    envoye_le = models.DateTimeField(auto_now_add=True, verbose_name='Envoyé le')
    inward = models.BooleanField(verbose_name='Vers l\'intérieur', help_text='Les messages vers l\'intérieur sont ceux qui sont envoyés par le client à un vendeur.')

    class Meta:
        verbose_name='message'

    def __str__(self):
        return f"Message #{self.id} dans {self.reclamation}"
