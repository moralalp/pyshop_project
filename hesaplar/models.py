from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.
class HesapYoneticisi(BaseUserManager):

    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Hesabın email adresi yok')

        if not username:
            raise ValueError('Hesabın kullanıcı adı yok')

        kullanici = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        kullanici.set_password(password)
        kullanici.save(using=self._db)
        return kullanici

    def create_superuser(self, first_name, last_name, username, email, password):
        kullanici = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        kullanici.is_admin = True
        kullanici.is_staff = True
        kullanici.is_active = True
        kullanici.is_superadmin = True
        kullanici.set_password(password)
        kullanici.save(using=self._db)
        return kullanici


class Hesap(AbstractBaseUser):
    first_name = models.CharField(verbose_name='İsim', max_length=50)
    last_name = models.CharField(verbose_name='Soyisim', max_length=50)
    username = models.CharField(verbose_name='Kullanıcı Adı', max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(verbose_name='Telefon numarası', max_length=50)

    date_joined = models.DateTimeField(verbose_name='Kayıt tarihi', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Son giriş tarihi', auto_now_add=True)
    is_admin = models.BooleanField(verbose_name='Admin', default=False)
    is_staff = models.BooleanField(verbose_name='Çalışan', default=False)
    is_active = models.BooleanField(verbose_name='Aktif', default=False)
    is_superadmin = models.BooleanField(verbose_name='Superadmin', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objeler = HesapYoneticisi()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    class Meta:
        verbose_name = 'Hesap'
        verbose_name_plural = 'Hesaplar'