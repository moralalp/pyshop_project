from django.contrib import admin
from .models import Marka


# Register your models here.
class MarkaAdmin(admin.ModelAdmin):
    prepopulated_fields = {'takma_marka_adi': ('marka_adi',)}
    list_display = ('marka_adi', 'takma_marka_adi')


admin.site.register(Marka, MarkaAdmin)