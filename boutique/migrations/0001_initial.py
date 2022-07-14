# Generated by Django 4.0.4 on 2022-05-13 08:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Commande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Constructeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='EtatCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Modele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('annee', models.IntegerField()),
                ('constructeur', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.constructeur')),
            ],
        ),
        migrations.CreateModel(
            name='Reclamation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('est_ouvert', models.BooleanField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.commande')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilClient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_entreprise', models.TextField()),
                ('adresse_ligne1', models.TextField()),
                ('adresse_ligne2', models.TextField()),
                ('code_postal', models.TextField()),
                ('ville', models.TextField()),
                ('telephone', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('descriptif', models.TextField()),
                ('prix_ttc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('stock', models.IntegerField()),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.categorie')),
                ('modeles_compatibles', models.ManyToManyField(to='boutique.modele')),
            ],
        ),
        migrations.CreateModel(
            name='MessageReclamation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sujet', models.TextField()),
                ('message', models.TextField()),
                ('inward', models.BooleanField()),
                ('reclamation', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.reclamation')),
            ],
        ),
        migrations.CreateModel(
            name='EntreeDeCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.commande')),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.produit')),
            ],
        ),
        migrations.AddField(
            model_name='commande',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.profilclient'),
        ),
        migrations.CreateModel(
            name='ChangementEtatCommande',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('commande', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.commande')),
                ('etat', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='boutique.etatcommande')),
            ],
        ),
    ]
