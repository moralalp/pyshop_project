from django.contrib import admin
from .models import Urun, Varyasyon


# Register your models here.
class MagazaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'takma_urun_adi': ('urun_adi',)}
    list_editable = ('stok',)
    list_display = (
    'urun_adi', 'takma_urun_adi', 'fiyat', 'indirimli_fiyat', 'stok', 'kategori', 'alt_kategori', 'marka',
    'duzenleme_tarihi', 'mevcut')


class VaryasyonAdmin(admin.ModelAdmin):
    list_display = ('urun_adi', 'varyasyon_kategori', 'varyasyon_degeri', 'stok', 'eklenecek_fiyat', 'aktif')
    list_editable = ('aktif', 'stok', 'eklenecek_fiyat')
    list_filter = ('urun__urun_adi', 'varyasyon_kategori', 'stok', 'varyasyon_degeri')


admin.site.register(Urun, MagazaAdmin)
admin.site.register(Varyasyon, VaryasyonAdmin)
