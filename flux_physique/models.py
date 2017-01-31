# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.contrib.auth.models import User
from refereces.models import StatutDocument, StatutProduit, Produit, Founisseur, Magasin, Emplacement, Client,\
    TypesMouvementStock, Employer


exercice = 2016


class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User)

    class Meta:
        abstract = True


class AchatsFournisseur(BaseModel):

    fournisseur = models.ForeignKey(Founisseur, verbose_name='Fournissur', on_delete=models.PROTECT)
    n_BL = models.CharField(max_length=15, verbose_name='Numéro de BL')
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    date_entree = models.DateField(verbose_name='Date de BL')
    n_FAC = models.CharField(max_length=15, verbose_name="Numéro de Facture d'achat", null=True)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    observation = models.TextField(max_length=200, null=True)
    validate_by = models.ForeignKey(User, null=True, blank=True, related_name='validation_achats')

    def __str__(self):
        return self.n_BL

    class Meta:
        permissions = (
            ("valider_achats", "Peut valider les achats"),
            ("voir_historique_achats", "Peut voir l'historique des achats"),
            ("importer_achats",'Peut importer les achats'),
            )


class DetailsAchatsFournisseur(BaseModel):

    entete = models.ForeignKey(AchatsFournisseur, on_delete=models.PROTECT)
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut Produit', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite', default=0)
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite', default=0)
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis', default=0)
    qtt = models.IntegerField(verbose_name='Quantité')
    ref_unique = models.CharField(max_length=20, verbose_name='reference_unique', default=0)

    def __str__(self):
        return self.produit.__str__()


class CommandesClient(BaseModel):
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    n_commande = models.CharField(max_length=10, verbose_name='Numéro de commande')
    date_commande = models.DateField(verbose_name='Date de la commande')
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)


class DetailsCommandeClient(BaseModel):

    commande_client = models.ForeignKey(CommandesClient, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    qtt = models.IntegerField(verbose_name='Quantité')


class FacturesClient(BaseModel):
    curr_exercice = models.IntegerField(default=exercice, verbose_name='Exrcice en cours')
    n_commande = models.CharField(max_length=10, verbose_name='Numéro de la facture')
    date_commande = models.DateField(verbose_name='Date de la facture')
    client = models.ForeignKey(Client, verbose_name='Client', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)


class DetailsFacturesClient(BaseModel):
    facture_client = models.ForeignKey(FacturesClient, on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    qtt = models.IntegerField(verbose_name='Quantité')


class Transfert(BaseModel):
    depuis_magasin = models.ForeignKey(Magasin, verbose_name='Depuis magasin', related_name='+',
                                       on_delete=models.PROTECT)
    vers_magasin = models.ForeignKey(Magasin, verbose_name='Vers magasin', on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    motif = models.ForeignKey(TypesMouvementStock, verbose_name='Motif du mouvement', default=1)
    validate_by = models.ForeignKey(User, null=True, blank=True, related_name='validation_name')

    class Meta:
        permissions = (
            ("valider_mouvements_stock", "Peut valider les mouvements de stocks"),
            ("transferer", "Peut transferer"),
            ("entreposer", "Peut Entreposer"),
            ("voir_historique_transferts", "Peut voir l'historique des transferts"),
            ("voir_stock", "Peut voir l'état du stock"),
            ("exporter_stock", "Peut exporter l'état du stock"),
            ("sortie_colis_complets", "Peut fair des sorties en colis d'origine"),
            )


class Stock(BaseModel):

    id_in_content_type = models.PositiveIntegerField(verbose_name='Id Stock')
    content_type = models.PositiveIntegerField(verbose_name='Contenent_type')
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Vente HT')
    taux_tva = models.IntegerField(verbose_name='TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Lot')
    date_peremption = models.DateField(verbose_name='DDP')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite')
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite')
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis')
    qtt = models.IntegerField(verbose_name='Quantité')
    motif = models.CharField(max_length=20, verbose_name='Transaction')
    recu = models.BooleanField(default=False, verbose_name='Reçu')


class DetailsTransfert(BaseModel):
    entete = models.ForeignKey(Transfert, on_delete=models.PROTECT)
    id_in_content_type = models.PositiveIntegerField(verbose_name='Id in content type')
    content_type = models.PositiveIntegerField(verbose_name='Contenent_type')
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut', on_delete=models.PROTECT)
    depuis_emplacement = models.ForeignKey(Emplacement, verbose_name='Depuis Empl', on_delete=models.PROTECT,
                                           related_name='depuis_empl')
    vers_emplacement = models.ForeignKey(Emplacement, verbose_name='Vers Empl', on_delete=models.PROTECT,
                                         related_name='vers_empl')
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Vente HT')
    taux_tva = models.IntegerField(verbose_name='TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Lot')
    date_peremption = models.DateField(verbose_name='DDP')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite')
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite')
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis')
    qtt = models.IntegerField(verbose_name='Quantité')


class MotifsInventaire(BaseModel):
    motif_inventaire = models.CharField(max_length=30, verbose_name="Motif de l'inventaire")

    def __str__(self):
        return self.motif_inventaire


class Inventaire(BaseModel):
    motif_inventaire = models.ForeignKey(MotifsInventaire, verbose_name="Motif de l'inventaire",
                                         on_delete=models.PROTECT)
    statut_doc = models.ForeignKey(StatutDocument, verbose_name='Statut du document', on_delete=models.PROTECT)
    description = models.CharField(max_length=200, verbose_name='Description')

    def __str__(self):
        return ' '.join(
            (self.motif_inventaire.__str__(), '-', str(self.id)))


class DetailsInventaire(BaseModel):
    entete = models.ForeignKey(Inventaire, on_delete=models.PROTECT)
    conformite = models.ForeignKey(StatutProduit, verbose_name='Statut Produit', on_delete=models.PROTECT)
    emplacement = models.ForeignKey(Emplacement, verbose_name='Emplacement', on_delete=models.PROTECT)
    produit = models.ForeignKey(Produit, verbose_name='Produit', on_delete=models.PROTECT)
    prix_achat = models.DecimalField(max_digits=9, decimal_places=2, verbose_name="Prix d'achat HT")
    prix_vente = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Prix de vente HT')
    taux_tva = models.IntegerField(verbose_name='Taux TVA')
    shp = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='SHP')
    ppa_ht = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='PPA')
    n_lot = models.CharField(max_length=20, verbose_name='Numéro du lot')
    date_peremption = models.DateField(verbose_name='Date de péremption')
    colisage = models.IntegerField(verbose_name='Colisage')
    poids_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids boite')
    volume_boite = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Volume boite')
    poids_colis = models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Poids du Colis')
    qtt = models.IntegerField(verbose_name='Quantité')


class EnteteTempo(BaseModel):

    transaction = models.CharField(max_length=30)


class Reservation(models.Model):
    entete_tempo = models.ForeignKey(EnteteTempo, on_delete=models.CASCADE, verbose_name='Entête de la réservation')
    id_stock = models.ForeignKey(Stock, verbose_name='Id Stock')
    qtt = models.IntegerField(verbose_name='Quantité réservée')
    new_emplacement = models.ForeignKey(Emplacement, null=True)


class Validation(BaseModel):
    id_in_content_type = models.PositiveIntegerField(verbose_name='Id in content type')
    content_type = models.PositiveIntegerField(verbose_name='Contenent type')
    boite_count = models.PositiveIntegerField(verbose_name='Nombre de boites')
    ligne_count = models.PositiveIntegerField(verbose_name='Nombre de lignes')

    def __str__(self):
        return ' '.join((str(self.id_in_content_type), str(self.content_type)))


class HistoriqueDuTravail(models.Model):
    id_validation = models.ForeignKey(Validation, on_delete=models.CASCADE, verbose_name='ID Validation')
    type = models.ForeignKey(TypesMouvementStock, verbose_name='Type du mouvement de stock', on_delete=models.PROTECT)
    employer = models.ForeignKey(Employer, verbose_name='Employer', on_delete=models.PROTECT)
    groupe = models.SmallIntegerField(verbose_name='Effectif du groupe')

    def __str__(self):
        return ' '.join(
            (self.employer.__str__(), self.groupe.__str__(), self.type.__str__())
                        )


class Parametres(models.Model):
    magasin_picking = models.ForeignKey(Magasin, verbose_name='Magasin de picking')
    emplacement_achat = models.ForeignKey(Emplacement, verbose_name='Emplacement de reception des achats')
    exercice = models.IntegerField(verbose_name='Exercice en cours')

@receiver(post_save, sender=DetailsAchatsFournisseur, dispatch_uid="add_achats_to_stock")
def add_achat_to_stock(sender, instance, created, **kwargs):
    if created == True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt = instance.qtt
        new_motif = 'Achat'
        new_created_by = instance.created_by

        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by=new_created_by
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsAchatsFournisseur, dispatch_uid="delete_achat_from_stock")
def delete_achat_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@transaction.atomic
@receiver(post_save, sender=DetailsTransfert, dispatch_uid="add_transfert_to_stock")
def add_transfert_to_stock(sender, instance, created, **kwargs):
    if created == True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.vers_emplacement
        old_emplacement = instance.depuis_emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt_in = instance.qtt
        new_motif = 'Transfert-In'
        new_created_by = instance.created_by
        new_obj1 = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt_in, motif=new_motif,
            created_by= new_created_by
        )

        new_qtt_out = -1*instance.qtt
        new_motif = 'Transfert-Out '
        new_obj2 = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=old_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt_out, motif=new_motif,
            created_by= new_created_by
        )
        new_obj1.save()
        new_obj2.save()

@receiver(post_delete, sender=DetailsTransfert, dispatch_uid="delete_transfert_from_stock")
def delete_transfert_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.filter(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@transaction.atomic
@receiver(post_save, sender=DetailsFacturesClient, dispatch_uid="add_achats_to_stock")
def add_vente_to_stock(sender, instance, created, **kwargs):
    if created == True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = StatutProduit.objects.get(statut='Conforme')
        new_emplacement = instance.produit.prelevement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.produit.poids
        new_volume_boite = instance.produit.volume
        new_poids_colis = 0
        new_qtt = -1*instance.qtt
        new_motif = 'Vente'
        new_created_by = instance.created_by
        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by= new_created_by
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsFacturesClient, dispatch_uid="delete_achat_from_stock")
def delete_vente_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@receiver(post_save, sender=DetailsInventaire, dispatch_uid="add_inventaire_to_stock")
def add_inventaire_to_stock(sender, instance, created, **kwargs):
    if created == True:
        new_id_stock = instance.id
        new_contenent_type = ContentType.objects.get_for_model(instance).id
        new_conformite = instance.conformite
        new_emplacement = instance.emplacement
        new_produit = instance.produit
        new_prix_achat = instance.prix_achat
        new_prix_vente = instance.prix_vente
        new_taux_tva = instance.taux_tva
        new_shp = instance.shp
        new_ppa_ht = instance.ppa_ht
        new_n_lot = instance.n_lot
        new_date_peremption = instance.date_peremption
        new_colisage = instance.colisage
        new_poids_boite = instance.poids_boite
        new_volume_boite = instance.volume_boite
        new_poids_colis = instance.poids_colis
        new_qtt = instance.qtt
        new_motif = 'Inventaire'
        new_created_by = instance.created_by

        new_obj = Stock(
            id_in_content_type=new_id_stock, content_type=new_contenent_type,
            conformite=new_conformite, emplacement=new_emplacement, produit=new_produit, prix_achat=new_prix_achat,
            prix_vente=new_prix_vente, taux_tva=new_taux_tva, shp=new_shp, ppa_ht=new_ppa_ht, n_lot=new_n_lot,
            date_peremption=new_date_peremption, colisage=new_colisage, poids_boite=new_poids_boite,
            volume_boite=new_volume_boite, poids_colis=new_poids_colis, qtt=new_qtt, motif=new_motif,
            created_by=new_created_by
        )
        new_obj.save()


@receiver(post_delete, sender=DetailsInventaire, dispatch_uid="delete_inventaire_from_stock")
def delete_inventaire_from_stock(sender, instance, **kwargs):
    contenent_type = ContentType.objects.get_for_model(instance).id
    obj = Stock.objects.get(id_in_content_type=instance.id, content_type=contenent_type)
    obj.delete()


@receiver(post_save, sender=Transfert, dispatch_uid="add_validation_transfert")
def add_validation_mvt_stock(sender, instance, created, **kwargs):
    if created == False:
        if instance.statut_doc_id == 2:
            contenent_type = ContentType.objects.get_for_model(instance).id
            id_in_content_type = instance.id
            linges_count = DetailsTransfert.objects.filter(entete=instance.id).count()
            boites_aggregaion = DetailsTransfert.objects.filter(entete=instance.id).all()
            total_qtt = 0
            for obj in boites_aggregaion:
                total_qtt += obj.qtt
            created_by = instance.validate_by
            obj = Validation(
                content_type=contenent_type,
                id_in_content_type=id_in_content_type,
                ligne_count=linges_count,
                boite_count=total_qtt,
                created_by=created_by
                     )
            obj.save()
@receiver(post_save, sender=AchatsFournisseur, dispatch_uid="add_validation_reception")
def add_validation_reception(sender, instance, created, **kwargs):
    if created == False:
        if instance.statut_doc_id == 2:
            contenent_type = ContentType.objects.get_for_model(instance).id
            id_in_content_type = instance.id
            linges_count = DetailsAchatsFournisseur.objects.filter(entete=instance.id).count()
            boites_aggregaion = DetailsAchatsFournisseur.objects.filter(entete=instance.id).all()
            total_qtt = 0
            for obj in boites_aggregaion:
                total_qtt += obj.qtt
            created_by = instance.validate_by
            validation_check = Validation.objects.filter(
                content_type=contenent_type,
                id_in_content_type=id_in_content_type
            )
            if validation_check:
                pass
            else:
                obj = Validation(
                    content_type=contenent_type,
                    id_in_content_type=id_in_content_type,
                    ligne_count=linges_count,
                    boite_count=total_qtt,
                    created_by=created_by
                    )
                obj.save()
