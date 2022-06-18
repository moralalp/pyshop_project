from django.shortcuts import render, get_object_or_404
from ustmenu.models import UstMenu
from kategori.models import Kategori, AltKategori


def anasayfa(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }

    return render(request, 'anasayfa.html', icerik)


def iletisim(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }

    return render(request, 'iletisim.html', icerik)
