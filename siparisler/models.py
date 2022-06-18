from django.db import models

from adresler.models import Adres
from hesaplar.models import Hesap
from magaza.models import Urun, Varyasyon
from kargo.models import Kargo


# Create your models here.
class Odeme(models.Model):
    kullanici = models.ForeignKey(Hesap, verbose_name='Kullanıcı', on_delete=models.CASCADE)
    odeme_id = models.CharField(verbose_name='Ödeme Id', max_length=100)
    odeme_sekli = models.CharField(verbose_name='Ödeme Şekli', max_length=100)
    odenen_miktar = models.CharField(verbose_name='Ödenen Miktar', max_length=100)
    durum = models.CharField(verbose_name='Durum', max_length=100)
    olusturma_tarihi = models.DateTimeField(verbose_name='Oluşturma Tarihi', auto_now_add=True)

    def __str__(self):
        return self.odeme_id

    class Meta:
        verbose_name = 'Ödeme'
        verbose_name_plural = 'Ödemeler'


class Siparis(models.Model):
    DURUM = (
        ('Yeni', 'Yeni'),
        ('Kabul', 'Kabul'),
        ('Kargolandı', 'Kargolandı'),
        ('Tamamlandı', 'Tamamlandı'),
        ('İptal', 'İptal'),
    )

    kullanici = models.ForeignKey(Hesap, verbose_name='Kullanıcı', on_delete=models.SET_NULL, null=True)
    odeme = models.ForeignKey(Odeme, verbose_name='Ödeme', on_delete=models.SET_NULL, blank=True, null=True)
    siparis_numarasi = models.CharField(verbose_name='Sipariş Numarası', max_length=20)
    kargo = models.ForeignKey(Kargo, verbose_name='Kargo', on_delete=models.SET_NULL, null=True)
    kargo_takip_numarasi = models.CharField(verbose_name='Kargo Takip Numarası', max_length=100, blank=True, null=True)
    adres = models.ForeignKey(Adres, verbose_name='Adres', on_delete=models.SET_NULL, null=True)
    order_note = models.CharField(verbose_name='Sipariş Notu', max_length=100, blank=True)
    siparis_toplami = models.FloatField(verbose_name='Sipariş Toplamı')
    durum = models.CharField(verbose_name='Durum', choices=DURUM, max_length=10, default='Yeni')
    ip = models.CharField(blank=True, max_length=20)
    siparis_verildi = models.BooleanField(verbose_name='Sipariş Verildi', default=False)
    olusturma_tarihi = models.DateTimeField(verbose_name='Oluşturma Tarihi', auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(verbose_name='Güncelleme Tarihi', auto_now=True)

    def __str__(self):
        return self.kullanici.first_name

    class Meta:
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'


class SiparisUrunu(models.Model):
    siparis = models.ForeignKey(Siparis, verbose_name='Sipariş', on_delete=models.CASCADE)
    odeme = models.ForeignKey(Odeme, verbose_name='Ödeme', on_delete=models.SET_NULL, blank=True, null=True)
    kullanici = models.ForeignKey(Hesap, verbose_name='Kullanıcı', on_delete=models.CASCADE)
    urun = models.ForeignKey(Urun, verbose_name='Ürün', on_delete=models.CASCADE)
    varyasyonlar = models.ManyToManyField(Varyasyon, verbose_name='Varyasyonlar', blank=True)
    adet = models.IntegerField(verbose_name='Adet')
    fiyat = models.FloatField(verbose_name='Fiyat')
    siparis_verildi = models.BooleanField(verbose_name='Sipariş Verildi', default=False)
    olusturma_tarihi = models.DateTimeField(verbose_name='Oluşturma Tarihi', auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(verbose_name='Güncelleme Tarihi', auto_now=True)

    def __str__(self):
        return self.urun.urun_adi

    class Meta:
        verbose_name = 'Sipariş Ürünü'
        verbose_name_plural = 'Sipariş Ürünleri'