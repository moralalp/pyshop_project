from django.db import models
from magaza.models import Urun, Varyasyon
from hesaplar.models import Hesap


# Create your models here.
class Sepet(models.Model):
    sepet_id = models.CharField(verbose_name='Sepet ID', max_length=250, blank=True)
    eklenme_tarihi = models.DateField(verbose_name='Eklenme Tarihi', auto_now_add=True)

    def __str__(self):
        return self.sepet_id

    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = 'Sepetler'


class SepetUrunu(models.Model):
    kullanici = models.ForeignKey(Hesap, verbose_name='Kullanıcı', on_delete=models.CASCADE, null=True)
    urun = models.ForeignKey(Urun, verbose_name='Ürün', on_delete=models.CASCADE)
    varyasyonlar = models.ManyToManyField(Varyasyon, blank=True)
    sepet = models.ForeignKey(Sepet, on_delete=models.CASCADE, null=True)
    adet = models.IntegerField()
    aktif = models.BooleanField(default=True)

    def ara_toplam(self):
        ara_toplam_fiyat = 0.0
        if self.urun.indirimli_fiyat:
            ara_toplam_fiyat += self.urun.indirimli_fiyat * self.adet
        else:
            ara_toplam_fiyat += self.urun.fiyat * self.adet
        for varyasyon in self.varyasyonlar.all():
            ara_toplam_fiyat += varyasyon.eklenecek_fiyat * self.adet
        return ara_toplam_fiyat

    def __str__(self):
        return self.urun.urun_adi

    class Meta:
        verbose_name = 'Sepet Ürünü'
        verbose_name_plural = 'Sepet Ürünleri'