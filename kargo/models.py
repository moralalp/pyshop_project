from django.db import models


# Create your models here.
class Kargo(models.Model):
    kargo_adi = models.CharField(verbose_name='Kategori Adı', max_length=100, unique=True)
    takma_kargo_adi = models.SlugField(verbose_name='Takma Kategori Adı', max_length=100, unique=True)
    eklenecek_fiyat = models.FloatField(verbose_name='Eklenecek Fiyat', default=0.0)
    ucretsiz_kargo_limiti = models.FloatField(verbose_name='Ücretsiz Kargo Limiti', default=0.0)
    kapida_odeme = models.BooleanField(verbose_name='Kapıda Ödeme', default=False)
    kargo_takip_linki = models.CharField(verbose_name='Kargo Takip Linki', max_length=255)

    def __str__(self):
        return self.kargo_adi

    class Meta:
        verbose_name = 'Kargo'
        verbose_name_plural = 'Kargolar'