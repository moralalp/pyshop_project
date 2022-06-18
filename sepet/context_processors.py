from .models import Sepet, SepetUrunu
from .views import _sepet_id


def sayac(request):
    sepet_sayaci = 0
    sepet_toplami = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            sepet = Sepet.objects.filter(sepet_id=_sepet_id(request))
            if request.user.is_authenticated:
                sepet_urunleri = SepetUrunu.objects.all().filter(kullanici=request.user)
            else:
                sepet_urunleri = SepetUrunu.objects.all().filter(sepet=sepet[:1])
            for sepet_urunu in sepet_urunleri:
                sepet_sayaci += sepet_urunu.adet
                if sepet_urunu.urun.indirimli_fiyat:
                    sepet_toplami += (sepet_urunu.urun.indirimli_fiyat * sepet_urunu.adet)
                else:
                    sepet_toplami += (sepet_urunu.urun.fiyat * sepet_urunu.adet)
        except Sepet.DoesNotExist:
            sepet_sayaci = 0
            sepet_toplami = 0
        return dict(sepet_sayaci=sepet_sayaci, sepet_toplami=sepet_toplami)