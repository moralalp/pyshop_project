from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Coalesce
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from ustmenu.models import UstMenu
from .models import Urun
from kategori.models import Kategori, AltKategori
from marka.models import Marka


# Create your views here.
def magaza(request, takma_kategori_adi=None, takma_alt_kategori_adi=None):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    kategori_adi = None

    if takma_kategori_adi is not None and takma_alt_kategori_adi is None:
        kategoriler = get_object_or_404(Kategori, takma_kategori_adi=takma_kategori_adi)
        urunler = Urun.objects.all().filter(kategori=kategoriler, mevcut=True)
        kategori_adi = kategoriler.kategori_adi
    elif takma_kategori_adi is not None and takma_alt_kategori_adi is not None:
        kategoriler = get_object_or_404(Kategori, takma_kategori_adi=takma_kategori_adi)
        alt_kategoriler = get_object_or_404(AltKategori, takma_alt_kategori_adi=takma_alt_kategori_adi)
        urunler = Urun.objects.all().filter(kategori=kategoriler, alt_kategori=alt_kategoriler, mevcut=True)
        kategori_adi = kategoriler.kategori_adi + ' / ' + alt_kategoriler.alt_kategori_adi
    else:
        urunler = Urun.objects.all().filter(mevcut=True)

    arama = request.GET.get('arama')

    if arama:
        urunler = urunler.all().filter(Q(urun_adi__icontains=arama) | Q(etiketler__icontains=arama)
                                       | Q(stok_kodu__icontains=arama) | Q(kategori__kategori_adi__icontains=arama)
                                       | Q(alt_kategori__alt_kategori_adi__icontains=arama))

    siralama = request.GET.get('sirala', default='maxtarih')

    if siralama == 'maxtarih':
        urunler = urunler.all().order_by('-eklenme_tarihi')
    elif siralama == 'mintarih':
        urunler = urunler.all().order_by('eklenme_tarihi')
    elif siralama == 'maxfiyat':
        urunler = urunler.all().annotate(son_fiyat=Coalesce('indirimli_fiyat', 'fiyat')).order_by('-son_fiyat')
    elif siralama == 'minfiyat':
        urunler = urunler.all().annotate(son_fiyat=Coalesce('indirimli_fiyat', 'fiyat')).order_by('son_fiyat')

    urun_sayisi = urunler.count()

    paginator = Paginator(urunler, 9)
    sayfa = request.GET.get('sayfa')
    sayfa_urunleri = paginator.get_page(sayfa)

    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
        'urunler': sayfa_urunleri,
        'urun_sayisi': urun_sayisi,
        'siralama': siralama,
        'kategori_adi': kategori_adi,
        'arama': arama
    }
    icerik.update(settings.GLOBAL_SETTINGS)
    return render(request, 'magaza/magaza.html', icerik)


def urun_detayi(request, takma_kategori_adi=None, takma_alt_kategori_adi=None, takma_urun_adi=None):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    try:
        urun = Urun.objects.get(kategori__takma_kategori_adi=takma_kategori_adi, alt_kategori__takma_alt_kategori_adi=takma_alt_kategori_adi, takma_urun_adi=takma_urun_adi)
    except Exception as e:
        raise e

    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
        'takma_kategori_adi': takma_kategori_adi,
        'takma_alt_kategori_adi': takma_alt_kategori_adi,
        'urun': urun
    }
    return render(request, 'magaza/urun_detayi.html', icerik)
