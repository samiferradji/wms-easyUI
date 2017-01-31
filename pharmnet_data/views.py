from dbfread import DBF
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render
from flux_physique.models import *
from pharmnet_data.forms import UploadFileForm
from refereces.models import *


@login_required(login_url='/login/')
@permission_required('flux_physique.importer_achats', raise_exception=True)
@transaction.atomic
def import_data(request):
    default_magasin_picking = Parametres.objects.get(id=1).magasin_picking
    default_emplacement_picking = Emplacement.objects.order_by('id').filter(
        magasin=default_magasin_picking).first().emplacement
    default_emplacement_recption = Parametres.objects.get(id=1).emplacement_achat
    username = ' '.join((request.user.first_name, request.user.last_name))
    user_id = request.user.id
    count_laboratoires = 0
    count_fournisseur = 0
    count_entete_achat = 0
    count_formes_pharmaceutiques = 0
    count_dci = 0
    count_produit = 0
    count_lignes_achat = 0
    count_emplacement = 0
    form = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            entete_file = request.FILES['entete_achats_file']
            details_file = request.FILES['details_achats_file']

            #  ******************fournisseurs**********************************

            with open('upload.dbf', 'wb+') as destination:
                for chunk in entete_file.chunks():
                    destination.write(chunk)
            db = DBF("upload.dbf", encoding='CP437')
            for data in db.records:
                new_dossier_fournisseur = data['ECFRS']
                new_designation_fournisseur = data['ELFRS']
                if not Founisseur.objects.filter(dossier__contains=new_dossier_fournisseur):
                    new_fournisseur = Founisseur(
                        dossier=new_dossier_fournisseur,
                        nom=new_designation_fournisseur
                    )
                    new_fournisseur.save()
                    count_fournisseur += 1
                new_entete_achat_id = data['ENMVT']
                new_date_mouvement = data['EDMVT']
                new_num_facture = data['ENFACT']
                if not AchatsFournisseur.objects.filter(n_BL__exact=new_entete_achat_id):
                    new_entete_obj = AchatsFournisseur(
                        fournisseur=Founisseur.objects
                        .get(dossier=new_dossier_fournisseur),
                        n_BL=new_entete_achat_id,
                        curr_exercice='2016',
                        date_entree=new_date_mouvement,
                        n_FAC=new_num_facture,
                        statut_doc_id=1,
                        observation='Importation PHARMNET',
                        created_by_id=user_id
                    )

                    new_entete_obj.save()
                    count_entete_achat += 1
            with open('upload.dbf', 'wb+') as destination:
                for chunk in details_file.chunks():
                    destination.write(chunk)
            db = DBF("upload.dbf", encoding=' CP437')
            for data in db.records:
                new_dossier_laboratoire = data['LFRS1']
                new_designation_laboratoire = data['LLIBFRS1']
                new_form_pharmaceutique_str = (data['LFORME']).replace('.', ' ')
                new_code_dci = str(data['LCDCI'])
                new_dci = data['LDCI']
                new_dosage = data['LDOSA']
                new_zone = data['LDEPOT']
                new_emplacement = data['LSDEPOT']
                new_emplacement_zone = new_zone + '.' + new_emplacement
                new_code_produit = data['LCPROD']
                new_produit = data['LCMRC']
                new_entete_achat_id = data['LNMVT']
                new_prix_achat = data['LPVU1']
                new_prix_vente = data['LPVU3']
                new_tva = data['LTVA']
                new_shp = data['LSHP4']
                new_ppa_ht = data['LPVU4A']
                new_n_lot = data['LNLOT']
                new_date_peremption = data['LPEREMP']
                new_colisage = data['LCOLISA']
                new_qtt = data['LQTE']
                new_reference_unique = ''.join(('2016', str(new_entete_achat_id), str(data['LSUIT'])))

                # ******************Laboratoire**********************************

                if not Laboratoire.objects.filter(dossier__exact=new_dossier_laboratoire):
                    new_fournisseur = Laboratoire(
                        dossier=new_dossier_laboratoire,
                        nom=new_designation_laboratoire
                    )
                    new_fournisseur.save()
                    count_laboratoires += 1

                # ******************formes pharmaceutiques**********************************

                if not FormePharmaceutique.objects.filter(forme__exact=new_form_pharmaceutique_str):
                    new_form_pharmaceutique = FormePharmaceutique(forme=new_form_pharmaceutique_str)
                    new_form_pharmaceutique.save()
                    count_formes_pharmaceutiques += 1

                # ******************DCI**********************************

                if not Dci.objects.filter(code_dci__exact=new_code_dci):
                    if len(new_code_dci) != 0:
                        new_dci_obj = Dci(
                            code_dci=new_code_dci,
                            dci=new_dci,
                            dosage=new_dosage,
                            forme_phrmaceutique=FormePharmaceutique.objects.get(
                                forme=new_form_pharmaceutique_str)
                        )
                        new_dci_obj.save()
                        count_dci += 1
                # *****************Emplacement**********************************

                if not Emplacement.objects.filter(emplacement__exact=new_emplacement_zone):
                    new_emplacement_obj = Emplacement(
                        emplacement=new_emplacement_zone,
                        magasin=default_magasin_picking
                    )
                    new_emplacement_obj.save()
                    count_emplacement += 1

                # *****************Produits**********************************
                if not Produit.objects.filter(code__exact=new_code_produit):
                    if new_emplacement_zone != '.':
                        emplacement_picking = new_emplacement_zone
                    else:

                        emplacement_picking = default_emplacement_picking
                    new_dci_obj = Produit(
                        code=new_code_produit,
                        produit=new_produit,
                        dci=Dci.objects.get(dci=new_dci),
                        laboratoire=Laboratoire.objects.get(dossier=new_dossier_laboratoire),
                        prelevement=Emplacement.objects.get(emplacement=emplacement_picking)
                    )
                    new_dci_obj.save()
                    count_produit += 1
                # *****************Lignes Achats**********************************
                if not DetailsAchatsFournisseur.objects.filter(
                        ref_unique__exact=new_reference_unique):
                    new_ligne_achat = DetailsAchatsFournisseur(
                        entete=AchatsFournisseur.objects.get(n_BL=new_entete_achat_id),
                        produit=Produit.objects.get(code=new_code_produit),
                        n_lot=new_n_lot,
                        conformite_id=1,
                        emplacement=default_emplacement_recption,
                        prix_achat=new_prix_achat,
                        prix_vente=new_prix_vente,
                        taux_tva=new_tva,
                        shp=new_shp,
                        ppa_ht=new_ppa_ht,
                        date_peremption=new_date_peremption,
                        colisage=new_colisage,
                        qtt=new_qtt,
                        ref_unique=new_reference_unique,
                        created_by_id=user_id
                    )
                    new_ligne_achat.save()
                    count_lignes_achat += 1
            return render(
                request,
                'pharmnet_data/import_list.html',
                {
                    'username': username,
                    'laboratoires': count_laboratoires,
                    'fournisseurs': count_fournisseur,
                    'achats': count_entete_achat,
                    'formes_pharmaceutique': count_formes_pharmaceutiques,
                    'dci': count_dci,
                    'count_produit': count_produit,
                    'count_lignes_achats': count_lignes_achat,
                    'count_emplacement': count_emplacement
                })
        else:
            return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})

    else:
        return render(request, 'pharmnet_data/import.html', {'form': form, 'username': username})
