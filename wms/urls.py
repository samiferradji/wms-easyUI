from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from flux_physique import views
from pharmnet_data.views import import_data
from django.conf import settings



admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', auth_views.login),
    url(r'^login/$', auth_views.login),
    url(r'^logout/$', views.logout_view),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^home/$', views.home, name='Home'),
    url(r'^add-transfert/', views.add_transfert, name='add-transfert'),
    url(r'^add-entete-reservation/', views.add_entete_reservation, name='add-entete-reservation'),
    url(r'^add-ligne-reservation/', views.add_ligne_reservation, name='add-ligne-reservation'),
    url(r'^reservation-table/', views.reservation_table, name='reservation-table'),
    url(r'^stock-disponible/', views.stock_disponible, name='stock-disponible'),
    url(r'^stock-disponible-vente/', views.stock_disponible_vente, name='stock-disponible-vente'),
    url(r'^qtt-disponible/', views.qtt_disponible, name='qtt-disponible'),
    url(r'^print_transfert/', views.print_transfert, name='print'),
    url(r'^print_entreposage/', views.print_entreposage, name='print-entreposage'),
    url(r'^validate-transaction-view/', views.validate_transaction_view, name='validate_transaction_view'),
    url(r'^validate-reception-view/', views.validate_receptipon_view, name='validate_reception_view'),
    url(r'^validate-transaction/', views.post_validation, name='validate_transaction'),
    url(r'^transactions-encours/', views.transactions_encours, name='transactions_encours'),
    url(r'^receptions-encours/', views.reception_encours, name='receptions_encours'),
    url(r'^get_employee_name/', views.return_emplyee_by_coderh, name='get_employee_name'),
    url(r'^add-entreposage/', views.add_entreposage, name='add-entreposage'),
    url(r'^add-sortie-colis/', views.add_sortie_en_colis, name='add-sortie-en-colis'),
    url(r'^add-entreposage-reservation/', views.add_entreposage_reservation, name='add-entreposage-reservation'),
    url(r'^entreposage-reservation-table/', views.entreposage_reservation_table, name='entreposage-reservation-table'),
    url(r'^entreposage-add-ligne-reservation/', views.entreposage_add_ligne_reservation,
        name='entreposage-add-ligne-reservation'),
    url(r'^raport-stock/', views.stock_par_magasin, name='raport-stock'),
    url(r'^raport-stock-categorie/', views.stock_par_categorie, name='raport-stock-categorie'),
    url(r'^list-mouvements/', views.list_mouvements, name='list-mouvements'),
    url(r'^details-par-mouvement/', views.details_par_mouvement, name='details-par-mouvement'),
    url(r'^list-achats/', views.list_achats, name='list-achats'),
    url(r'^stock-csv/', views.stock_csv, name='stock-csv'),
    url(r'^produits-par-magasin/', views.produits_par_magasin, name='produits-par-magasin'),
    url(r'^liste-des-emplacements/', views.list_des_emplacement, name='liste-des-emplacements'),
    url(r'^liste-des-produit/', views.list_des_produit, name='liste-des-produit'),
    url(r'^import/', import_data),
    url(r'^base2/', views.base2),
)
urlpatterns += staticfiles_urlpatterns()
urlpatterns  += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

