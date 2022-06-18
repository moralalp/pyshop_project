from django.contrib import admin
from .models import Kategori, AltKategori


# Register your models here.
class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'takma_kategori_adi': ('kategori_adi',)}
    list_display = ('kategori_adi', 'takma_kategori_adi')


class AltKategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'takma_alt_kategori_adi': ('alt_kategori_adi',)}
    list_display = ('alt_kategori_adi', 'takma_alt_kategori_adi')


admin.site.register(Kategori, KategoriAdmin)
admin.site.register(AltKategori, AltKategoriAdmin)