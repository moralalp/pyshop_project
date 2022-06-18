from django.db import models


# Create your models here.
class Marka(models.Model):
    marka_adi = models.CharField(verbose_name='Marka Adı', max_length=50, unique=True)
    takma_marka_adi = models.SlugField(verbose_name='Takma Marka Adı', max_length=100, unique=True)
    aciklama = models.TextField(verbose_name='Açıklama', max_length=500)
    marka_resmi = models.ImageField(verbose_name='Marka Resmi', upload_to='resimler/markalar')

    def __str__(self):
        return self.marka_adi

    class Meta:
        verbose_name = 'Marka'
        verbose_name_plural = 'Markalar'