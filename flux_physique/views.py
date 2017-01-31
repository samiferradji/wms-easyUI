# -*- coding: utf-8 -*-
import csv
import operator
from datetime import date, timedelta, datetime
from functools import reduce

from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from django.db.models import Sum, Min, When, Case
from django_ajax.decorators import ajax
from django.forms import modelform_factory
from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from flux_physique.models import *
from flux_physique.forms import TransfertModelForm, ProductModelForm, EntreposageModelForm
from flux_physique.crud import commit_transaction, validate_transaction
from refereces.models import DepuisMagasinsAutorise, Employer


# *************************************************************************************************
#                                        general views
# *************************************************************************************************


@login_required(login_url='/login/')
def home(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    return render(request, 'home.html', {'username': username})

def base2(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    return render(request, 'base2.html', {'username': username})

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@ajax
@login_required(login_url='/login/')
def produits_par_magasin(request):
    key_words = request.POST['key_words']
    key_words_list = key_words.split(' ')
    current_magasin_id=int(request.POST['current_magasin_id'])
    queryset = Stock.objects.all().distinct().values('produit_id','produit__produit').filter(
        reduce(operator.and_, (Q(produit__produit__icontains=x) for x in key_words_list))).filter(emplacement__magasin_id=current_magasin_id).order_by('produit__produit')
    return queryset

@ajax
def list_des_produit(request):
    q = request.GET['q']
    keys_list = q.split(' ')
    maxRows = int(request.GET['maxRows'])
    query = Produit.objects.all().values('id','produit').order_by(
        'produit').filter( reduce(operator.and_, (Q(produit__icontains=x) for x in keys_list))
                               )[:maxRows]
    return query


# *****************************************************************************************************
#                                       Transfert de produits
# *****************************************************************************************************
@login_required(login_url='/login/')
@permission_required('flux_physique.transferer', raise_exception=True)
def add_transfert(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    user = request.user
    product_form = ProductModelForm()
    form = TransfertModelForm(user=user)
    return render(request, 'flux_physique/add_transfert.html', {'form': form, 'product_form': product_form,
                                                  'user': user, 'username': username})

@login_required(login_url='/login/')
@permission_required('flux_physique.sortie_colis_complets', raise_exception=True)
def add_sortie_en_colis(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    user = request.user
    product_form = ProductModelForm()
    form = TransfertModelForm(user=user)
    return render(request, 'flux_physique/add_sortie_colis.html', {'form': form, 'product_form': product_form,
                                                  'user': user, 'username': username})


@ajax
@permission_required('flux_physique.transferer', raise_exception=True)
@login_required(login_url='/login/')
def print_transfert(request):
    type_mouvement = 'Transfert'
    id_transfert = int(request.POST['id_transfert'])
    transfert = Transfert.objects.get(id=id_transfert)
    details_transfert = DetailsTransfert.objects.filter(entete=transfert).values(
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
        'n_lot',
        'date_peremption',
        'ppa_ht',
        'depuis_emplacement__emplacement',
        'vers_emplacement__emplacement',
        'colisage',
        'conformite__statut',
        'qtt'
    ).order_by('depuis_emplacement__emplacement')
    for obj in details_transfert:
        if obj['colisage'] !=0:
            obj['vrac'] = int(obj['qtt']) % int(obj['colisage'])
            obj['colis'] = int(obj['qtt']) // int(obj['colisage'])
        else:
            obj['colis'] = 0
            obj['vrac'] = obj['qtt']
    return render(
        request,
        'flux_physique/print.html',
        {
            'transfer': transfert,
            'details_transfert': details_transfert,
            'type_mouvement':type_mouvement
        })


# *****************************************************************************************************
#                                       Entreposage de produits
# *****************************************************************************************************


@login_required(login_url='/login/')
@permission_required('flux_physique.entreposer', raise_exception=True)
def add_entreposage(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    user = request.user
    product_form = ProductModelForm()
    form = EntreposageModelForm(user=user)
    return render(request, 'flux_physique/add_entreposage.html', {'form': form, 'product_form': product_form,
                                                  'user': user, 'username': username})


@ajax
@login_required(login_url='/login/')
def print_entreposage(request):
    type_mouvement = 'Entreposage'
    id_transfert = int(request.POST['id_transfert'])
    transfert = Transfert.objects.get(id=id_transfert)
    details_transfert = DetailsTransfert.objects.filter(entete=transfert).values(
        'id',
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
        'n_lot',
        'date_peremption',
        'ppa_ht',
        'depuis_emplacement__emplacement',
        'vers_emplacement__emplacement',
        'colisage',
        'conformite__statut',
        'qtt'
    )
    for obj in details_transfert:
        if obj['colisage'] !=0:
            obj['vrac'] = int(obj['qtt']) % int(obj['colisage'])
            obj['colis'] = int(obj['qtt']) // int(obj['colisage'])
        else:
            obj['colis'] = 0
            obj['vrac'] = obj['qtt']
    return render(
        request,
        'flux_physique/print.html',
        {
            'transfer': transfert,
            'details_transfert': details_transfert,
            'type_mouvement':type_mouvement})


@ajax
@permission_required('flux_physique.entreposer', raise_exception=True)
@login_required(login_url='/login/')
def add_entreposage_reservation(request):
    entete_reservation_form = modelform_factory(EnteteTempo, fields=['created_by', 'transaction', ])
    if request.method == "POST":
        current_magasin = request.POST['current_magasin']
        emplacements = Emplacement.objects.all().filter(
            magasin_id=current_magasin
        ).order_by('emplacement').values()
        form = entete_reservation_form(request.POST)
        if form.is_valid():
            new_tempo_id = form.save()
            return {'new_id':new_tempo_id.id,'emplacements':emplacements}
        else:
            return False
    return False


@permission_required('flux_physique.entreposer', raise_exception=True)
@login_required(login_url='/login/')
@ajax
def entreposage_reservation_table(request):  # TODO filter on product conformity
    current_entete = request.GET['current_entete']
    queryset = Reservation.objects.values_list(
        'id_stock__produit__produit',
        'id_stock__produit__dci__dosage',
        'id_stock__produit__dci__forme_phrmaceutique__forme',
        'id_stock__produit__conditionnement',
        'id_stock__n_lot',
        'id_stock__date_peremption',
        'id_stock__ppa_ht',
        'new_emplacement__emplacement',
        'new_emplacement__magasin__magasin',
        'id_stock__colisage',
        'qtt',
        'id'
    ).filter(entete_tempo__id=current_entete)
    reservation_list = []
    for item in queryset:
        item_list = list(item)
        ddp = item_list[5].isoformat()
        ppa = str(item_list[6])
        item_list[6] = ppa
        item_list[5] = ddp
        if item_list[9] !=0:
            vrac = int(item_list[10]) % (item_list[9])
            item_list.append(vrac)
            colis = int(item_list[10]) // (item_list[9])
            item_list.append(colis)
        else:
            vrac = item_list[10]
            item_list.append(vrac)
            colis =  0
        item_list.append(colis)

        reservation_list.append(item_list)

    return reservation_list


@ajax
def list_des_emplacement(request):
    q = request.GET['q']
    keys_list = q.split(' ')
    maxRows = int(request.GET['maxRows'])
    query = Emplacement.objects.all().values('id','emplacement').order_by(
        'emplacement').filter( reduce(operator.and_, (Q(emplacement__icontains=x) for x in keys_list))
                               )[:maxRows]
    return query


@permission_required('flux_physique.entreposer', raise_exception=True)
@login_required(login_url='/login/')
@ajax
def entreposage_add_ligne_reservation(request):
    details_reservation_form = modelform_factory(Reservation, fields=['entete_tempo', "id_stock", 'qtt','new_emplacement'])
    if request.method == "POST":
        if request.POST['action'] == 'add':
            id_stock = int(request.POST['id_stock'])
            qtt = int(request.POST['qtt'])
            if check_qtt_disponible(id_stock=id_stock, qtt=qtt) == True:
                form = details_reservation_form(request.POST)
                if form.is_valid():
                    form.save()
                    return 'OK'
                else:
                    print(form.errors)
            else:
                return check_qtt_disponible(id_stock=id_stock, qtt=qtt)

# *****************************************************************************************************
#                                       Concurences et reservations
# *****************************************************************************************************

@login_required(login_url='/login/')
@ajax
def add_entete_reservation(request):
    entete_reservation_form = modelform_factory(EnteteTempo, fields=['created_by', 'transaction', ])
    if request.method == "POST":
        form = entete_reservation_form(request.POST)
        if form.is_valid():
            new_tempo_id = form.save()

            return [new_tempo_id.id, ]
        else:
            return [str(form.errors)]


def sum_qtt_reserved(id_stock):
    try:
        total = Reservation.objects.values('id_stock').annotate(sum_reserved=Sum('qtt')).get(
            id_stock=id_stock
        )['sum_reserved']
        return total
    except :
        return 0


def check_qtt_disponible(id_stock, qtt):
    obj_stock = Stock.objects.get(id=id_stock)
    queryset = Stock.objects.values('id').filter(n_lot=obj_stock.n_lot,
                                                 date_peremption=obj_stock.date_peremption,
                                                 ppa_ht=obj_stock.ppa_ht,
                                                 emplacement=obj_stock.emplacement,
                                                 conformite=obj_stock.conformite
                                                 ).annotate(
        sum_totale=Sum(
            Case(
                When(Q(recu=True) | (Q(recu=False) and Q(motif='Transfert-Out')), then='qtt'),
                default=0)
            )

        )
    sum_reserved = int(sum_qtt_reserved(id_stock))
    sum_totale = 0
    for obj in queryset:
        sum_totale += int(obj['sum_totale'])
    qtt_dispo = sum_totale - sum_reserved
    if qtt > qtt_dispo :
        return ' '.join(('Quantité disponible : ',str(qtt_dispo)))
    if qtt < 0:
        return 'Quantité négative non acceptée'
    else:
        return True


@login_required(login_url='/login/')
@ajax
def add_ligne_reservation(request):
    details_reservation_form = modelform_factory(Reservation, fields=['entete_tempo', "id_stock", 'qtt'])
    if request.method == "POST":
        if request.POST['action'] == 'add':
            id_stock = int(request.POST['id_stock'])
            qtt = int(request.POST['qtt'])
            if check_qtt_disponible(id_stock=id_stock, qtt=qtt) == True:
                form = details_reservation_form(request.POST)
                if form.is_valid():
                    form.save()
                    return 'OK'
                else:
                    return [form.errors]
            else:
                return check_qtt_disponible(id_stock=id_stock, qtt=qtt)

        elif request.POST['action'] == 'delete':
            try:
                id_reservation = int(request.POST['id_reservation'])
                obj = Reservation.objects.get(id=id_reservation)
                obj.delete()
                return 'OK'
            except:
                return False
        elif request.POST['action'] == 'cancel':
            try:
                current_entete = request.POST['current_entete']
                current_entete = current_entete
                objs = EnteteTempo.objects.get(id=current_entete)
                objs.delete()
                return 'OK'
            except:
                return False
        elif request.POST['action'] == 'save_transfert':
            user = request.user
            entete_tempo = int(request.POST['current_entete'])
            depuis_magasin = int(request.POST['depuis_magasin'])
            vers_magasin = int(request.POST['vers_magasin'])
            motif = int(request.POST['motif'])
            saved = commit_transaction(
                transaction_type="save_transfert",
                user=user,
                depuis_magasin=depuis_magasin,
                vers_magasin=vers_magasin,
                entete_tempo=entete_tempo,
                motif=motif
            )
            return saved
        elif request.POST['action'] == 'save_entreposage':
            user = request.user
            entete_tempo = int(request.POST['current_entete'])
            depuis_magasin = int(request.POST['depuis_magasin'])
            vers_magasin = int(request.POST['vers_magasin'])
            motif = int(request.POST['motif'])
            saved = commit_transaction(
                transaction_type="save_entreposage",
                user=user,
                depuis_magasin=depuis_magasin,
                vers_magasin=vers_magasin,
                entete_tempo=entete_tempo,
                motif=motif
            )
            return saved


@login_required(login_url='/login/')
@ajax
def reservation_table(request):
    current_entete = request.GET['current_entete']
    queryset = Reservation.objects.values_list(
        'id_stock__produit__produit',
        'id_stock__produit__dci__dosage',
        'id_stock__produit__dci__forme_phrmaceutique__forme',
        'id_stock__produit__conditionnement',
        'id_stock__n_lot',
        'id_stock__date_peremption',
        'id_stock__ppa_ht',
        'id_stock__emplacement__emplacement',
        'id_stock__emplacement__magasin__magasin',
        'id_stock__colisage',
        'qtt',
        'id'
    ).filter(entete_tempo__id=current_entete)
    reservation_list = []
    for item in queryset:
        item_list = list(item)
        ddp = item_list[5].isoformat()
        ppa = str(item_list[6])
        item_list[6] = ppa
        item_list[5] = ddp
        if item_list[9] !=0:
            vrac = int(item_list[10]) % (item_list[9])
            item_list.append(vrac)
            colis = int(item_list[10]) // (item_list[9])
            item_list.append(colis)
        else:
            vrac = item_list[10]
            item_list.append(vrac)
            colis = 0
            item_list.append(colis)

        reservation_list.append(item_list)

    return reservation_list


@login_required(login_url='/login/')
@ajax
def stock_disponible(request):
    product_id = request.GET['current_produit']
    current_magasin = request.GET.get('current_magasin', None)
    user = request.user.id
    current_status_produit = StatutProduit.objects.filter(statutsautorise__user_id=user).values_list('id')
    queryset = Stock.objects.values(
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
        'n_lot',
        'date_peremption',
        'ppa_ht',
        'emplacement__emplacement',
        'emplacement__magasin__magasin',
        'colisage',
        'conformite__statut',
    ).filter(produit_id=product_id, emplacement__magasin_id=current_magasin,
             conformite_id__in=current_status_produit
             ).order_by('date_peremption').annotate(
        first_id=Min('id'),
        sum_totale=Sum(
            Case(
                When(Q(recu=True), then='qtt'), default=0)),
        sum_disponible=Sum(
            Case(
                When(Q(recu=True) | Q(motif='Transfert-Out'), then='qtt'), default=0)),
        sum_encours_out=Sum(
            Case(
                When(Q(recu=False) & Q(motif='Transfert-Out'), then='qtt'), default=0)),
        sum_encours_in=Sum(
            Case(
                When(Q(recu=False) & Q(motif='Transfert-In'), then='qtt'), default=0))
    ).filter(~Q(sum_encours_in__exact=0)|~Q(sum_totale__exact=0)|~Q(sum_encours_out__exact=0))
    for obj in queryset:
        obj['date_peremption'] = obj['date_peremption'].isoformat()
        obj['ppa_ht'] = str(obj['ppa_ht'])
        if obj['colisage'] !=0:
            obj['vrac'] = int(obj['sum_disponible']) % (obj['colisage'])
            obj['colis'] = int(obj['sum_disponible']) // (obj['colisage'])
        else:
            obj['colis'] = 0
            obj['vrac'] = obj['sum_disponible']
        current_id_stock = int(obj['first_id'])
        obj['sum_reserved'] = sum_qtt_reserved(current_id_stock)
    return queryset


@login_required(login_url='/login/')
@ajax
def stock_disponible_vente(request): # todo developper un interface vente
    product_id = request.GET['current_produit']
    user = request.user.id
    authorised_magasins = Magasin.objects.filter(depuismagasinsautorise__user=user).values_list('id')
    current_status_produit = StatutProduit.objects.filter(statutsautorise__user_id=user).values_list('id')
    queryset = Stock.objects.values(
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
        'n_lot',
        'date_peremption',
        'ppa_ht',
        'emplacement__emplacement',
        'emplacement__magasin__magasin',
        'colisage',
        'conformite__statut',
    ).filter(produit_id=product_id, emplacement__magasin_id__in=authorised_magasins,
             conformite_id__in=current_status_produit
             ).annotate(
        first_id=Min('id'),
        sum_totale=Sum(
            Case(
                When(Q(recu=True), then='qtt'), default=0)),
        sum_disponible=Sum(
            Case(
                When(Q(recu=True) | Q(motif='Transfert-Out'), then='qtt'), default=0)),
        sum_encours=Sum(
            Case(
                When(recu=False, then='qtt'), default=0)),
    )
    for obj in queryset:
        obj['date_peremption'] = obj['date_peremption'].isoformat()
        obj['ppa_ht'] = str(obj['ppa_ht'])
        if obj['colisage'] !=0:
            obj['vrac'] = int(obj['sum_disponible']) % (obj['colisage'])
            obj['colis'] = int(obj['sum_disponible']) // (obj['colisage'])
        else:
            obj['colis'] = 0
            obj['vrac'] = obj['sum_disponible']
        current_id_stock = int(obj['first_id'])
        obj['sum_reserved'] = sum_qtt_reserved(current_id_stock)
        current_id_stock = int(obj['first_id'])
        obj['sum_reserved'] = sum_qtt_reserved(current_id_stock)
    return queryset


@login_required(login_url='/login/')
@ajax
def qtt_disponible(request):  # aficher les produits disponibles pour le transfert
    id_stock = int(request.GET['current_id_stock'])
    obj_stock = Stock.objects.get(id=id_stock)
    if id_stock:
        queryset = Stock.objects.values(
            'n_lot',
            'date_peremption',
            'ppa_ht',
            'colisage',
            'conformite__statut',
        ).filter(n_lot=obj_stock.n_lot,
             date_peremption=obj_stock.date_peremption,
             ppa_ht=obj_stock.ppa_ht,
             emplacement=obj_stock.emplacement,
             conformite=obj_stock.conformite
             ).annotate(
        sum_totale=Sum(
            Case(
                When(Q(recu=True) | Q(motif='Transfert-Out'), then='qtt'), default=0)),
            )
        for obj in queryset:
            obj['date_peremption'] = obj['date_peremption'].isoformat()
            obj['ppa_ht'] = str(obj['ppa_ht'])
            obj['sum_reserved'] = sum_qtt_reserved(id_stock)
            obj['sum_disponible'] = obj['sum_totale'] - obj['sum_reserved']
            if obj['colisage'] !=0:
                obj['vrac'] = int(obj['sum_disponible']) % (obj['colisage'])
                obj['colis'] = int(obj['sum_disponible']) // (obj['colisage'])
            else:
                obj['colis'] = 0
                obj['vrac'] = obj['sum_disponible']

        return queryset


# *****************************************************************************************************
#                                       Validation des transactions
# *****************************************************************************************************

@permission_required('flux_physique.valider_mouvements_stock', raise_exception=True)
@login_required(login_url='/login/')
def validate_transaction_view(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    return render(request, 'flux_physique/validate_transaction.html', {'username': username})


@permission_required('flux_physique.valider_achats', raise_exception=True)
@login_required(login_url='/login/')
def validate_receptipon_view(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    return render(request, 'flux_physique/validate_reception.html', {'username': username})


@ajax
@login_required(login_url='/login/')
def post_validation(request):
    id_transaction = request.POST['id_transaction']
    if not id_transaction:
        return 'Veuillez saisir un N° valide'
    type_transaction = request.POST['type_transaction']
    if type_transaction == "check_id_transfert":
        transaction = Transfert.objects.filter(id=id_transaction, statut_doc_id=1)
        if transaction.count()==1:
            return 'OK'
        else:
            return 'Veuillez saisir un N° valide'
    if type_transaction == "check_id_achat":
        transaction = AchatsFournisseur.objects.filter(n_BL=id_transaction, statut_doc_id=1)
        if transaction.count()==1:
            return 'OK'
        else:
            return 'Veuillez saisir un N° valide'
    created_by = request.POST['created_by']
    code_rh1 = request.POST['code_RH1']
    code_rh2 = request.POST['code_RH2']
    code_rh3 = request.POST['code_RH3']
    validate_transaction(
        id_transaction=id_transaction,
        type_transaction=type_transaction,
        created_by=created_by,
        code_RH1=code_rh1,
        code_RH2=code_rh2,
        code_RH3=code_rh3,
    )



@ajax
@permission_required('flux_physique.valider_mouvements_stock', raise_exception=True)
@login_required(login_url='/login/')
def transactions_encours(request):
    magasin_autorise = DepuisMagasinsAutorise.objects.filter(user=request.user).values_list('magasins_id')
    transfert = Transfert.objects.filter(vers_magasin_id__in=magasin_autorise, statut_doc=1).values_list(
        'id',
        'depuis_magasin__magasin',
        'vers_magasin__magasin',
        'statut_doc__statut',
        'created_by__username'

    ).order_by('id').reverse()
    return transfert


@ajax
@permission_required('flux_physique.valider_achats', raise_exception=True)
@login_required(login_url='/login/')
def reception_encours(request):
    reception = AchatsFournisseur.objects.filter(statut_doc=1).values(
        'id',
        'n_BL',
        'date_entree',
        'fournisseur__nom',
        'n_FAC',
        'observation',
        'statut_doc__statut',
        'created_by__first_name',
        'created_by__last_name'
    ).order_by('id').reverse()
    for obj in reception:
        obj['date_entree'] = obj['date_entree'].isoformat()
    return reception


@ajax
@login_required(login_url='/login/')
def return_emplyee_by_coderh(request):
    code_rh = request.GET['code_RH']
    if code_rh:
        employee_count = Employer.objects.filter(code_RH=code_rh).count()

        if employee_count != 0:
            employee = Employer.objects.get(code_RH=code_rh)
            return ['OK', employee]
        else:
            return ['PAS OK', 'Code RH  introuvable']

    else:
        return 'VIDE'



# *****************************************************************************************************
#                                       Rapport Stock
# *****************************************************************************************************

@ajax
@permission_required('flux_physique.voir_stock', raise_exception=True)
def stock_par_categorie(request):
    if request.method == 'POST':
        categorie = request.POST['categorie']
        if categorie == 'produit_par_emplacement':
            current_produit_id = request.POST['current_produit']
            queryset = Stock.objects.values(
                'produit__produit',
                'produit__dci__dosage',
                'produit__dci__forme_phrmaceutique__forme',
                'produit__conditionnement',
                'n_lot',
                'date_peremption',
                'ppa_ht',
                'emplacement__emplacement',
                'emplacement__magasin__magasin',
                'colisage',
                'conformite__statut',
            ).filter(produit=current_produit_id, recu=True).annotate(Sum('qtt')).order_by(
                'emplacement__magasin__magasin',
                'emplacement__emplacement',
                'date_peremption',
            )
            for obj in queryset:
                obj['date_peremption'] = obj['date_peremption'].isoformat()
                obj['ppa_ht'] = str(obj['ppa_ht'])
                if obj['colisage'] != 0:
                    obj['vrac'] = int(obj['qtt__sum']) % (obj['colisage'])
                    obj['colis'] = int(obj['qtt__sum']) // (obj['colisage'])
                else:
                    obj['colis'] = 0
                    obj['vrac'] = obj['qtt__sum']
            return queryset

@permission_required('flux_physique.voir_stock', raise_exception=True)
def stock_par_magasin(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    filtre =''
    query = Stock.objects.values(
        'produit',
        'produit__code',
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
    ).filter(recu=True).annotate(Sum('qtt')).order_by('produit__produit')
    if request.method =='POST':
        filtre = request.POST['filtre']
        query = query.filter(produit__produit__icontains=filtre)
    paginator = Paginator(query, 15)
    page = request.GET.get('page')
    try:
        stock_page = paginator.page(page)
    except PageNotAnInteger:
        stock_page = paginator.page(1)
    except EmptyPage:
        stock_page = paginator.page(paginator.num_pages)


    return render(request, 'flux_physique/rapport_stock.html', {'stock':stock_page, 'filtre':filtre, 'username':username})


# *****************************************************************************************************
#                                       Historique Transfert , Achats et entreposage
# *****************************************************************************************************

@ajax
def details_par_mouvement(request):
    if request.method == 'POST':
        categorie = request.POST['categorie']
        if categorie == 'detail_par_bon':
            current_mouvement_id = request.POST['current_mouvement_id']
            queryset = DetailsTransfert.objects.values(
                'produit__produit',
                'produit__dci__dosage',
                'produit__dci__forme_phrmaceutique__forme',
                'produit__conditionnement',
                'n_lot',
                'date_peremption',
                'ppa_ht',
                'depuis_emplacement__emplacement',
                'vers_emplacement__emplacement',
                'colisage',
                'conformite__statut',
                'qtt'
            ).filter(entete=current_mouvement_id)
            for obj in queryset:
                obj['date_peremption'] = obj['date_peremption'].isoformat()
                obj['ppa_ht'] = str(obj['ppa_ht'])
            return queryset
        if categorie == 'print':
            type_mouvement = 'Mouvement'
            id_mouvement = request.POST['current_mouvement_id']
            mouvement = Transfert.objects.get(id=id_mouvement)
            details_transfert = DetailsTransfert.objects.filter(entete=mouvement).values(
                'produit__produit',
                'produit__dci__dosage',
                'produit__dci__forme_phrmaceutique__forme',
                'produit__conditionnement',
                'n_lot',
                'date_peremption',
                'ppa_ht',
                'depuis_emplacement__emplacement',
                'vers_emplacement__emplacement',
                'colisage',
                'conformite__statut',
                'qtt'
            ).order_by('depuis_emplacement__emplacement')
            for obj in details_transfert:
                if obj['colisage'] !=0:
                    obj['vrac'] = int(obj['qtt']) % int(obj['colisage'])
                    obj['colis'] = int(obj['qtt']) // int(obj['colisage'])
                else:
                    obj['vrac'] = obj['qtt']
                    obj['colis'] = 0
            return render(request, 'flux_physique/print.html',
                          {
                              'transfer': mouvement,
                              'details_transfert': details_transfert,
                              'type_mouvement': type_mouvement
                          })
        if categorie == 'print_reception':
            type_mouvement = 'Reception'
            id_mouvement = request.POST['current_mouvement_id']
            mouvement = AchatsFournisseur.objects.get(id=id_mouvement)
            details_achat = DetailsAchatsFournisseur.objects.filter(entete=mouvement).values(
                'id',
                'produit__produit',
                'produit__dci__dosage',
                'produit__dci__forme_phrmaceutique__forme',
                'produit__conditionnement',
                'n_lot',
                'date_peremption',
                'prix_achat',
                'prix_vente',
                'taux_tva',
                'shp',
                'ppa_ht',
                'emplacement__emplacement',
                'colisage',
                'conformite__statut',
                'qtt'
            ).order_by('id')
            for obj in details_achat:
                if obj['colisage'] != 0:
                    obj['vrac'] = int(obj['qtt']) % int(obj['colisage'])
                    obj['colis'] = int(obj['qtt']) // int(obj['colisage'])
                else:
                    obj['vrac'] = obj['qtt']
                    obj['colis'] = 0
            return render(request, 'flux_physique/print_achats.html',
                          {
                              'recption': mouvement,
                              'details_reception': details_achat,
                              'type_mouvement': type_mouvement
                          })

@permission_required('flux_physique.voir_historique_transferts', raise_exception=True)
def list_mouvements(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    date_fin = date.today()
    delta_date = timedelta(days=30)
    one_day = timedelta(days=1)
    date_debut = date_fin - delta_date
    date_fin_adjusted = date_fin + one_day
    date_debut = date_debut.isoformat()
    date_fin = date_fin.isoformat()
    if request.method =='POST':
        date_debut = request.POST['from_date']
        date_fin = request.POST['to_date']
        items = date_fin.split('-')
        items[2] = int(items[2])+1
        date_fin_adjusted = items[0] + '-' + items[1]+'-'+str(items[2])
    query = Transfert.objects.values(
        'id',
        'created_date',
        'depuis_magasin__magasin',
        'vers_magasin__magasin',
        'statut_doc__statut',
        'motif__type',
        'created_by__first_name',
        'created_by__last_name',
    ).order_by('id').reverse().filter(created_date__range=[date_debut, date_fin_adjusted])
    paginator = Paginator(query, 20)
    page = request.GET.get('page')
    try:
        mouvements_page = paginator.page(page)
    except PageNotAnInteger:
        mouvements_page = paginator.page(1)
    except EmptyPage:
        mouvements_page = paginator.page(paginator.num_pages)

    return render(request, 'flux_physique/historique_mouvement.html',
                  {
                      'mouvements':mouvements_page,
                      'from_date':date_debut,
                      'to_date': date_fin,
                      'username':username
                  })

@permission_required('flux_physique.voir_historique_achats', raise_exception=True)
def list_achats(request):
    username = ' '.join((request.user.first_name, request.user.last_name))
    date_fin = date.today()
    delta_date = timedelta(days=30)
    one_day = timedelta(days=1)
    date_debut = date_fin - delta_date
    date_fin_adjusted = date_fin + one_day
    date_debut = date_debut.isoformat()
    date_fin = date_fin.isoformat()
    if request.method == 'POST':
        date_debut = request.POST['from_date']
        date_fin = request.POST['to_date']
        items = date_fin.split('-')
        items[2] = int(items[2]) + 1
        date_fin_adjusted = items[0] + '-' + items[1] + '-' + str(items[2])
    query = AchatsFournisseur.objects.values(
        'id',
        'created_date',
        'n_BL',
        'date_entree',
        'n_FAC',
        'fournisseur__nom',
        'observation',
        'statut_doc__statut',
        'created_by__first_name',
        'created_by__last_name',
    ).order_by('id').reverse().filter(created_date__range=[date_debut, date_fin_adjusted])
    paginator = Paginator(query, 20)
    page = request.GET.get('page')
    try:
        mouvements_page = paginator.page(page)
    except PageNotAnInteger:
        mouvements_page = paginator.page(1)
    except EmptyPage:
        mouvements_page = paginator.page(paginator.num_pages)

    return render(request, 'flux_physique/historique_achats.html',
                  {
                      'mouvements':mouvements_page,
                      'from_date':date_debut,
                      'to_date': date_fin,
                      'username':username
                  })

@permission_required('flux_physique.exporter_stock', raise_exception=True)
def stock_csv(request):
    d = str(datetime.now())
    filename = 'stock au '+d+'.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
    response.write(u'\ufeff'.encode('utf8'))
    writer = csv.writer(response, delimiter=';')
    queryset = Stock.objects.values_list(
        'produit__produit',
        'produit__dci__dosage',
        'produit__dci__forme_phrmaceutique__forme',
        'produit__conditionnement',
        'n_lot',
        'date_peremption',
        'ppa_ht',
        'emplacement__emplacement',
        'emplacement__magasin__magasin',
        'colisage',
        'conformite__statut',
    ).annotate(Sum('qtt')).order_by('produit__produit').filter(recu=True)
    stock = []
    for obj in queryset:
        obj = list(obj)
        if obj[9] != 0:
            colis = int(obj[11]) % (obj[9])
            vrac = int(obj[11]) // (obj[9])
            obj.append(colis)
            obj.append(vrac)
            stock.append(obj)
        else:
            colis = 0
            vrac = obj[11]
            obj.append(colis)
            obj.append(vrac)
            stock.append(obj)
    writer.writerow(
        ['Produit',
         'Dosage',
         'Forme',
         'Conditionnement',
         'Lot',
         'DDP',
         'PPA',
         'Emplacement',
         'Magasin',
         'Colisage',
         'Statut',
         'Qtt',
         'Colis',
         'Vrac'
         ]
    )
    for obj in stock:
        row = []
        for field in obj:
            row.append(field)
        writer.writerow(row)
    return response
