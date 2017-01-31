from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from refereces.models import *
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin

admin.site.site_title = 'LOCAPRO 5'
admin.site.site_header = 'LOCAPRO 5'

@admin.register(FormePharmaceutique)
class FormAdmin(ImportExportModelAdmin):
    pass

admin.site.register(Axe)
admin.site.register(Wilaya)
admin.site.register(Commune)
admin.site.register(Client)
admin.site.register(StatutDocument)
admin.site.register(StatutProduit)
admin.site.register(Dci)
admin.site.register(Magasin)
admin.site.register(Emplacement)
admin.site.register(Founisseur)
admin.site.register(Laboratoire)
admin.site.register(Produit)
admin.site.register(TypesMouvementStock)
admin.site.register(Employer)
admin.site.register(TypeEntreposage)



class DepuisMagasinsInline(admin.TabularInline):
    model = DepuisMagasinsAutorise
    extra = 1

class VersMagasinsInline(admin.TabularInline):
    model = VersMagasinsAutorise
    extra = 1

class StatutsInline(admin.TabularInline):
    model = StatutsAutorise
    extra = 1

class UserAdmin(AuthUserAdmin):
   def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(UserAdmin, self).add_view(*args, **kwargs)

   def change_view(self, *args, **kwargs):
      self.inlines = [DepuisMagasinsInline, VersMagasinsInline, StatutsInline]
      return super(UserAdmin, self).change_view(*args, **kwargs)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

