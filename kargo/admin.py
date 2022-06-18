from django.contrib import admin
from .models import Kargo


# Register your models here.
class KargoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'takma_kargo_adi': ('kargo_adi',)}
    list_display = ('kargo_adi', 'takma_kargo_adi')


admin.site.register(Kargo, KargoAdmin)