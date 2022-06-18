from django.db import models
from kategori.models import Kategori


# Create your models here.
class UstMenu(models.Model):
    menu_adi = models.ForeignKey(Kategori, verbose_name='Menü Adı', unique=True, on_delete=models.CASCADE)
    alt_menuler = models.BooleanField(verbose_name='Alt Menüleri Göster', default=True)

    def __str__(self):
        return self.menu_adi.kategori_adi

    class Meta:
        verbose_name = 'Üst Menü'
        verbose_name_plural = 'Üst Menüler'