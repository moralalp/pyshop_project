from django.db import models
from django.core.exceptions import ValidationError
from kategori.models import Kategori, AltKategori
from marka.models import Marka


# Create your models here.
class Urun(models.Model):
    urun_adi = models.CharField(verbose_name='Ürün Adı', max_length=200, unique=True)
    takma_urun_adi = models.SlugField(verbose_name='Takma Ürün Adı', max_length=200, unique=True)
    aciklama = models.TextField(verbose_name='Açıklama', max_length=500)
    fiyat = models.FloatField(verbose_name='Fiyat')
    indirimli_fiyat = models.FloatField(verbose_name='İndirimli Fiyat', blank=True, null=True)
    urun_resmi = models.ImageField(verbose_name='Ürün Resmi', upload_to='resimler/ürünler')
    stok = models.IntegerField()
    stok_kodu = models.CharField(verbose_name='Stok Kodu', max_length=200, unique=True)
    mevcut = models.BooleanField(default=True)
    kategori = models.ForeignKey(Kategori, verbose_name='Kategori', on_delete=models.CASCADE)
    alt_kategori = models.ForeignKey(AltKategori, verbose_name='Alt Kategori', blank=True, null=True,
                                     on_delete=models.CASCADE)
    marka = models.ForeignKey(Marka, verbose_name='Marka', on_delete=models.CASCADE)
    etiketler = models.CharField(verbose_name='Etiketler', max_length=200)
    eklenme_tarihi = models.DateTimeField(verbose_name='Eklenme Tarihi', auto_now_add=True)
    duzenleme_tarihi = models.DateTimeField(verbose_name='Düzenleme Tarihi', auto_now=True)

    def __str__(self):
        return self.urun_adi

    class Meta:
        verbose_name = 'Ürün'
        verbose_name_plural = 'Ürünler'


class Varyasyon(models.Model):
    urun = models.ForeignKey(Urun, verbose_name='Ürün', on_delete=models.CASCADE)
    varyasyon_kategori = models.CharField(verbose_name='Varyasyon Kategorisi', max_length=100)
    varyasyon_degeri = models.CharField(verbose_name='Varyasyon Değeri', max_length=100)
    eklenecek_fiyat = models.FloatField(verbose_name='Eklenecek Fiyat', default=0.0)
    varyasyon_kirilimi = models.ForeignKey('self', verbose_name='Varyasyon Kırılımı', blank=True, null=True, on_delete=models.CASCADE)
    aktif = models.BooleanField(default=True)
    eklenme_tarihi = models.DateTimeField(verbose_name='Eklenme Tarihi', auto_now_add=True)
    stok = models.IntegerField()
    stok_kodu = models.CharField(verbose_name='Varyasyon Stok Kodu', max_length=200, unique=True)

    def clean(self):
        if self.varyasyon_kirilimi and (self.urun != self.varyasyon_kirilimi.urun):
            raise ValidationError("Lütfen varyasyon kırılımı için aynı ürünü seçiniz.")

    def __str__(self):
        return self.urun.urun_adi + ' ' + self.varyasyon_kategori + ' ' + self.varyasyon_degeri

    @property
    def urun_adi(self):
        return self.urun.urun_adi

    class Meta:
        verbose_name = 'Varyasyon'
        verbose_name_plural = 'Varyasyonlar'