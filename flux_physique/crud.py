# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from flux_physique.models import Transfert, Reservation, DetailsTransfert, EnteteTempo, Stock, HistoriqueDuTravail,\
    Validation, DetailsAchatsFournisseur, AchatsFournisseur, Parametres
from refereces.models import Emplacement, StatutDocument, Magasin, Employer



@transaction.atomic
def commit_transaction(transaction_type=None, user=None, depuis_magasin=None, vers_magasin=None,
                       entete_tempo=None, motif=None):
    if transaction_type == 'save_transfert':
            user = user
            entete_tempo = entete_tempo
            depuis_magasin = depuis_magasin
            vers_magasin = vers_magasin
            default_emplacement = Emplacement.objects.filter(magasin_id=vers_magasin).order_by('id').first()
            default_statut = StatutDocument.objects.order_by('id').first()
            reservation_details = Reservation.objects.filter(entete_tempo=entete_tempo).all()
            if reservation_details:
                new_transfert = Transfert(
                    created_by=user,
                    depuis_magasin=Magasin.objects.get(id=depuis_magasin),
                    vers_magasin=Magasin.objects.get(id=vers_magasin),
                    statut_doc=default_statut,
                    motif_id=motif)
                new_transfert.save()
                for item in reservation_details:
                    if vers_magasin == Parametres.objects.get(id=1).magasin_picking_id:
                        new_transfert_details = DetailsTransfert(
                            created_by=user,
                            entete=new_transfert,
                            id_in_content_type=item.id_stock.id_in_content_type,
                            content_type=item.id_stock.content_type,
                            conformite=item.id_stock.conformite,
                            depuis_emplacement=item.id_stock.emplacement,
                            vers_emplacement=item.id_stock.produit.prelevement,
                            produit=item.id_stock.produit,
                            prix_achat=item.id_stock.prix_achat,
                            prix_vente=item.id_stock.prix_vente,
                            taux_tva=item.id_stock.taux_tva,
                            shp=item.id_stock.shp,
                            ppa_ht=item.id_stock.ppa_ht,
                            n_lot=item.id_stock.n_lot,
                            date_peremption=item.id_stock.date_peremption,
                            colisage=item.id_stock.colisage,
                            poids_boite=item.id_stock.poids_boite,
                            volume_boite=item.id_stock.volume_boite,
                            poids_colis=item.id_stock.poids_colis,
                            qtt=item.qtt,
                        )
                        new_transfert_details.save()
                    else:
                        new_transfert_details = DetailsTransfert(
                            created_by=user,
                            entete=new_transfert,
                            id_in_content_type=item.id_stock.id_in_content_type,
                            content_type=item.id_stock.content_type,
                            conformite=item.id_stock.conformite,
                            depuis_emplacement=item.id_stock.emplacement,
                            vers_emplacement=default_emplacement,
                            produit=item.id_stock.produit,
                            prix_achat=item.id_stock.prix_achat,
                            prix_vente=item.id_stock.prix_vente,
                            taux_tva=item.id_stock.taux_tva,
                            shp=item.id_stock.shp,
                            ppa_ht=item.id_stock.ppa_ht,
                            n_lot=item.id_stock.n_lot,
                            date_peremption=item.id_stock.date_peremption,
                            colisage=item.id_stock.colisage,
                            poids_boite=item.id_stock.poids_boite,
                            volume_boite=item.id_stock.volume_boite,
                            poids_colis=item.id_stock.poids_colis,
                            qtt=item.qtt,
                            )
                        new_transfert_details.save()
                    entete_tempo_obj = EnteteTempo.objects.filter(id=entete_tempo)
                    entete_tempo_obj.delete()
                return ['OK',new_transfert.id]
    if transaction_type == 'save_entreposage':
            user = user
            entete_tempo = entete_tempo
            depuis_magasin = depuis_magasin
            vers_magasin = vers_magasin
            default_statut = StatutDocument.objects.order_by('id').first()
            reservation_details = Reservation.objects.filter(entete_tempo=entete_tempo).all()
            if reservation_details:
                new_transfert = Transfert(
                    created_by=user,
                    depuis_magasin=Magasin.objects.get(id=depuis_magasin),
                    vers_magasin=Magasin.objects.get(id=vers_magasin),
                    statut_doc=default_statut,
                    motif_id=motif
                )
                new_transfert.save()
                for item in reservation_details:
                    new_transfert_details = DetailsTransfert(
                        created_by=user,
                        entete=new_transfert,
                        id_in_content_type=item.id_stock.id_in_content_type,
                        content_type=item.id_stock.content_type,
                        conformite=item.id_stock.conformite,
                        depuis_emplacement=item.id_stock.emplacement,
                        vers_emplacement=item.new_emplacement,
                        produit=item.id_stock.produit,
                        prix_achat=item.id_stock.prix_achat,
                        prix_vente=item.id_stock.prix_vente,
                        taux_tva=item.id_stock.taux_tva,
                        shp=item.id_stock.shp,
                        ppa_ht=item.id_stock.ppa_ht,
                        n_lot=item.id_stock.n_lot,
                        date_peremption=item.id_stock.date_peremption,
                        colisage=item.id_stock.colisage,
                        poids_boite=item.id_stock.poids_boite,
                        volume_boite=item.id_stock.volume_boite,
                        poids_colis=item.id_stock.poids_colis,
                        qtt=item.qtt,
                        )
                    new_transfert_details.save()
                    entete_tempo_obj = EnteteTempo.objects.filter(id=entete_tempo)
                    entete_tempo_obj.delete()
                return ['OK',new_transfert.id]

@transaction.atomic
def validate_transaction(type_transaction=None, id_transaction=None, created_by=None,
                         code_RH1=None, code_RH2=None, code_RH3=None):
    if type_transaction =="transfert":
        details_contenent_type = ContentType.objects.get_for_model(DetailsTransfert).id
        transfert_contenent_type = ContentType.objects.get_for_model(Transfert).id
        transfert_obj = Transfert.objects.get(id=id_transaction)
        transfert_obj.statut_doc_id = 2
        transfert_obj.validate_by_id = created_by
        transfert_obj.save()
        motif_mouvement = transfert_obj.motif.id
        id_details_transfert = DetailsTransfert.objects.filter(entete=id_transaction).values_list('id')
        Stock.objects.filter(content_type=details_contenent_type,
                             id_in_content_type__in=id_details_transfert).update(recu=True)
        current_validation = Validation.objects.get(id_in_content_type=id_transaction,
                                                    content_type=transfert_contenent_type)
        groupe = 0
        if code_RH1:
            groupe +=1
        if code_RH2:
            groupe += 1
        if code_RH3:
            groupe += 1
        if code_RH1:
            employer = Employer.objects.get(code_RH=code_RH1)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=motif_mouvement,  # 1 pour transfert
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()
        if code_RH2:
            employer = Employer.objects.get(code_RH=code_RH2)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=motif_mouvement,  # 1 pour transfert
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()
        if code_RH3:
            employer = Employer.objects.get(code_RH=code_RH3)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=motif_mouvement,  # 1 pour transfert
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()

        return 'OK'

    if type_transaction =="reception":
        details_contenent_type = ContentType.objects.get_for_model(DetailsAchatsFournisseur).id
        reception_contenent_type = ContentType.objects.get_for_model(AchatsFournisseur).id
        reception_obj = AchatsFournisseur.objects.get(n_BL=id_transaction)
        reception_obj.statut_doc_id = 2
        reception_obj.validate_by_id = created_by
        reception_obj.save()
        id_details_reception = DetailsAchatsFournisseur.objects.filter(entete=reception_obj.id).values_list('id')
        Stock.objects.filter(content_type=details_contenent_type,
                             id_in_content_type__in=id_details_reception).update(recu=True)
        current_validation = Validation.objects.get(id_in_content_type=reception_obj.id,
                                                    content_type=reception_contenent_type)
        groupe = 0
        if code_RH1:
            groupe +=1
        if code_RH2:
            groupe += 1
        if code_RH3:
            groupe += 1
        if code_RH1:
            employer = Employer.objects.get(code_RH=code_RH1)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=2,  # 1 pour transfert, 2 pour reception
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()
        if code_RH2:
            employer = Employer.objects.get(code_RH=code_RH2)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=2,  # 1 pour transfert, 2 pour reception
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()
        if code_RH3:
            employer = Employer.objects.get(code_RH=code_RH3)
            new_execution = HistoriqueDuTravail(
                employer=employer,
                type_id=2,  # 1 pour transfert, 2 pour reception
                groupe=groupe,
                id_validation=current_validation
            )
            new_execution.save()

        return 'OK'
    else:
        return 'PAS OK'





