from django.contrib import admin
from .models import Sepet, SepetUrunu


# Register your models here.
class SepetAdmin(admin.ModelAdmin):
    list_display = ('sepet_id', 'eklenme_tarihi')


class SepetUrunuAdmin(admin.ModelAdmin):
    list_display = ('urun', 'sepet', 'adet', 'aktif')


admin.site.register(Sepet, SepetAdmin)
admin.site.register(SepetUrunu, SepetUrunuAdmin)
