# Generated by Django 4.0.4 on 2022-05-13 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boutique', '0004_messagereclamation_envoye_le_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='changementetatcommande',
            name='etat',
            field=models.CharField(choices=[('new', 'Nouvelle'), ('acc', 'Acceptée'), ('dec', 'Refusée'), ('sen', 'Expédiée'), ('dis', 'Livrée'), ('can', 'Annulée')], max_length=3),
        ),
    ]
