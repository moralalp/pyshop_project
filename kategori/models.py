from django.db import models
from django.urls import reverse


# Create your models here.
class Kategori(models.Model):
    kategori_adi = models.CharField(verbose_name='Kategori Adı', max_length=50, unique=True)
    takma_kategori_adi = models.SlugField(verbose_name='Takma Kategori Adı', max_length=100, unique=True)
    aciklama = models.TextField(verbose_name='Açıklama', max_length=500)
    kategori_resmi = models.ImageField(verbose_name='Kategori Resmi', upload_to='resimler/kategoriler')

    def __str__(self):
        return self.kategori_adi

    def link_getir(self):
        return reverse('kategoriye_gore_urunler', args=[self.takma_kategori_adi])

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'


class AltKategori(models.Model):
    alt_kategori_adi = models.CharField(verbose_name='Alt Kategori Adı', max_length=50, unique=True)
    ust_kategori = models.ForeignKey(verbose_name='Üst Kategori', to=Kategori, on_delete=models.CASCADE)
    takma_alt_kategori_adi = models.SlugField(verbose_name='Takma Alt Kategori Adı', max_length=100, unique=True)
    aciklama = models.TextField(verbose_name='Açıklama', max_length=500)
    alt_kategori_resmi = models.ImageField(verbose_name='Alt Kategori Resmi', upload_to='resimler/alt_kategoriler')

    def __str__(self):
        return self.alt_kategori_adi

    def link_getir(self):
        return reverse('alt_kategoriye_gore_urunler', args=[self.ust_kategori.takma_kategori_adi, self.takma_alt_kategori_adi])

    class Meta:
        verbose_name = 'Alt Kategori'
        verbose_name_plural = 'Alt Kategoriler'
