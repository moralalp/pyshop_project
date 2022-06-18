from django.db import models
from hesaplar.models import Hesap


# Create your models here.
class Adres(models.Model):
    kullanici = models.ForeignKey(Hesap, verbose_name='Kullanıcı', on_delete=models.SET_NULL, null=True)
    address_title = models.CharField(verbose_name='Adres Başlığı', max_length=50)
    first_name = models.CharField(verbose_name='İsim', max_length=50)
    last_name = models.CharField(verbose_name='Soyisim', max_length=50)
    phone = models.CharField(verbose_name='Telefon', max_length=15)
    email = models.CharField(verbose_name='Email', max_length=50)
    address_line_1 = models.CharField(verbose_name='Adres Satırı 1', max_length=50)
    address_line_2 = models.CharField(verbose_name='Adres Satırı 2', max_length=50, blank=True)
    country = models.CharField(verbose_name='Ülke', max_length=50)
    state = models.CharField(verbose_name='İlçe', max_length=50)
    city = models.CharField(verbose_name='İl', max_length=50)
    post_code = models.CharField(verbose_name='Posta Kodu', max_length=15)

    def __str__(self):
        return self.kullanici.email

    class Meta:
        verbose_name = 'Adres'
        verbose_name_plural = 'Adresler'