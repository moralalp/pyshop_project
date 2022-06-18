from .models import Kategori, AltKategori


def yan_menu_kategori_linkleri(request):
    kategori_linkleri = Kategori.objects.all().order_by('kategori_adi')
    return dict(kategori_linkleri=kategori_linkleri)


def yan_menu_alt_kategori_linkleri(request):
    alt_kategori_linkleri = AltKategori.objects.all().order_by('alt_kategori_adi')
    return dict(alt_kategori_linkleri=alt_kategori_linkleri)