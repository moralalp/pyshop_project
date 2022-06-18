from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from magaza.models import Urun, Varyasyon
from sepet.models import Sepet, SepetUrunu
from ustmenu.models import UstMenu
from kategori.models import Kategori, AltKategori
from django.contrib.auth.decorators import login_required
from kargo.models import Kargo
from adresler.models import Adres


# Create your views here.
# _ is intended for internal use
# __ is private function
def _sepet_id(request):
    sepet = request.session.session_key
    if not sepet:
        sepet = request.session.create()
    return sepet


def sepete_ekle(request, urun_id):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    mevcut_kullanici = request.user

    if mevcut_kullanici.is_authenticated:
        urun = Urun.objects.get(id=urun_id)
        urun_adeti = request.POST.get('urun_adeti')

        urun_varyasyonlari = []
        varyasyon_kirilimlari = []

        for item in request.POST:
            key = item
            if key == 'urun_adeti':
                continue
            value = request.POST[key]

            try:
                varyasyon = Varyasyon.objects.get(urun=urun, id=value)
                urun_varyasyonlari.append(varyasyon)
            except:
                pass

        for dıs_varyasyon in urun_varyasyonlari:
            counter = 0
            ic_varyasyon = dıs_varyasyon
            while True:
                ic_varyasyon = ic_varyasyon.varyasyon_kirilimi
                if ic_varyasyon:
                    counter += 1
                else:
                    varyasyon_kirilimlari.append(counter)
                    break

        if len(urun_varyasyonlari) > 0:
            son_varyasyon_index = varyasyon_kirilimlari.index(max(varyasyon_kirilimlari))

        if urun_adeti is None:
            urun_adeti = 1
        elif int(urun_adeti) <= 0:
            hata = 'Sepete 0 ya da daha düşük adette ürün ekleyemezsiniz'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)

        if len(urun_varyasyonlari) > 0 and int(urun_varyasyonlari[son_varyasyon_index].stok) < int(urun_adeti):
            hata = 'Sepete istediğiniz seçeneklerde yalnızca ' + str(
                urun_varyasyonlari[son_varyasyon_index].stok) + ' adet ürün ekleyebilirsiniz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)
        elif len(urun_varyasyonlari) == 0 and int(urun.stok) < int(urun_adeti):
            hata = 'Sepete istediğiniz üründen yalnızca ' + str(urun.stok) + ' adet ekleyebilirsiniz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)

        sepet_urunu_bulundu = SepetUrunu.objects.filter(urun=urun, kullanici=mevcut_kullanici).exists()
        if sepet_urunu_bulundu:
            sepet_urunu = SepetUrunu.objects.filter(urun=urun, kullanici=mevcut_kullanici)
            eski_varyasyon_listesi = []
            id = []
            for item in sepet_urunu:
                mevcut_varyasyonlar = item.varyasyonlar.all()
                eski_varyasyon_listesi.append(list(mevcut_varyasyonlar))
                id.append(item.id)
            if urun_varyasyonlari in eski_varyasyon_listesi:
                index = eski_varyasyon_listesi.index(urun_varyasyonlari)
                item_id = id[index]
                item = SepetUrunu.objects.get(urun=urun, id=item_id)
                item.adet += int(urun_adeti)
            else:
                item = SepetUrunu.objects.create(
                    urun=urun,
                    adet=int(urun_adeti),
                    kullanici=mevcut_kullanici
                )
                if len(urun_varyasyonlari) > 0:
                    item.varyasyonlar.clear()
                    item.varyasyonlar.add(*urun_varyasyonlari)
            item.save()
        else:
            sepet_urunu = SepetUrunu.objects.create(
                urun=urun,
                adet=int(urun_adeti),
                kullanici=mevcut_kullanici
            )
            if len(urun_varyasyonlari) > 0:
                sepet_urunu.varyasyonlar.clear()
                sepet_urunu.varyasyonlar.add(*urun_varyasyonlari)
            sepet_urunu.save()
        return redirect('sepet')
    else:
        urun = Urun.objects.get(id=urun_id)
        urun_adeti = request.POST.get('urun_adeti')

        urun_varyasyonlari = []
        varyasyon_kirilimlari = []

        for item in request.POST:
            key = item
            if key == 'urun_adeti':
                continue
            value = request.POST[key]

            try:
                varyasyon = Varyasyon.objects.get(urun=urun, id=value)
                urun_varyasyonlari.append(varyasyon)
            except:
                pass

        for dıs_varyasyon in urun_varyasyonlari:
            counter = 0
            ic_varyasyon = dıs_varyasyon
            while True:
                ic_varyasyon = ic_varyasyon.varyasyon_kirilimi
                if ic_varyasyon:
                    counter += 1
                else:
                    varyasyon_kirilimlari.append(counter)
                    break

        if len(urun_varyasyonlari) > 0:
            son_varyasyon_index = varyasyon_kirilimlari.index(max(varyasyon_kirilimlari))

        if urun_adeti is None:
            urun_adeti = 1
        elif int(urun_adeti) <= 0:
            hata = 'Sepete 0 ya da daha düşük adette ürün ekleyemezsiniz'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)

        if len(urun_varyasyonlari) > 0 and int(urun_varyasyonlari[son_varyasyon_index].stok) < int(urun_adeti):
            hata = 'Sepete istediğiniz seçeneklerde yalnızca ' + str(urun_varyasyonlari[son_varyasyon_index].stok) + ' adet ürün ekleyebilirsiniz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)
        elif len(urun_varyasyonlari) == 0 and int(urun.stok) < int(urun_adeti):
            hata = 'Sepete istediğiniz üründen yalnızca ' + str(urun.stok) + ' adet ekleyebilirsiniz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata
            }
            return render(request, 'hata.html', icerik)

        try:
            sepet = Sepet.objects.get(sepet_id=_sepet_id(request))
        except Sepet.DoesNotExist:
            sepet = Sepet.objects.create(
                sepet_id=_sepet_id(request)
            )
        sepet.save()

        sepet_urunu_bulundu = SepetUrunu.objects.filter(urun=urun, sepet=sepet).exists()
        if sepet_urunu_bulundu:
            sepet_urunu = SepetUrunu.objects.filter(urun=urun, sepet=sepet)
            eski_varyasyon_listesi = []
            id = []
            for item in sepet_urunu:
                mevcut_varyasyonlar = item.varyasyonlar.all()
                eski_varyasyon_listesi.append(list(mevcut_varyasyonlar))
                id.append(item.id)
            if urun_varyasyonlari in eski_varyasyon_listesi:
                index = eski_varyasyon_listesi.index(urun_varyasyonlari)
                item_id = id[index]
                item = SepetUrunu.objects.get(urun=urun, id=item_id)
                item.adet += int(urun_adeti)
            else:
                item = SepetUrunu.objects.create(
                    urun=urun,
                    adet=int(urun_adeti),
                    sepet=sepet
                )
                if len(urun_varyasyonlari) > 0:
                    item.varyasyonlar.clear()
                    item.varyasyonlar.add(*urun_varyasyonlari)
            item.save()
        else:
            sepet_urunu = SepetUrunu.objects.create(
                urun=urun,
                adet=int(urun_adeti),
                sepet=sepet
            )
            if len(urun_varyasyonlari) > 0:
                sepet_urunu.varyasyonlar.clear()
                sepet_urunu.varyasyonlar.add(*urun_varyasyonlari)
            sepet_urunu.save()
        return redirect('sepet')


def sepetten_sil(request, urun_id):
    sepet_urunu = SepetUrunu.objects.get(id=urun_id)
    sepet_urunu.delete()
    return redirect('sepet')


def sepeti_guncelle(request):
    if request.user.is_authenticated:
        sepet_urunleri = SepetUrunu.objects.filter(kullanici=request.user)
    else:
        sepet = Sepet.objects.get(sepet_id=_sepet_id(request))
        sepet_urunleri = SepetUrunu.objects.all().filter(sepet=sepet)
    for sepet_urunu in sepet_urunleri:
        try:
            urun = SepetUrunu.objects.get(id=sepet_urunu.id)
            istenen_adet = int(request.POST.get(str(sepet_urunu.id)))
        except:
            continue

        urun_varyasyonlari = urun.varyasyonlar.all()
        varyasyon_kirilimlari = []

        for dıs_varyasyon in urun_varyasyonlari:
            counter = 0
            ic_varyasyon = dıs_varyasyon
            while True:
                ic_varyasyon = ic_varyasyon.varyasyon_kirilimi
                if ic_varyasyon:
                    counter += 1
                else:
                    varyasyon_kirilimlari.append(counter)
                    break

        if len(urun_varyasyonlari) > 0:
            son_varyasyon_index = varyasyon_kirilimlari.index(max(varyasyon_kirilimlari))

        if len(urun_varyasyonlari) > 0 and int(urun_varyasyonlari[son_varyasyon_index].stok) < istenen_adet:
            urun.adet = int(urun_varyasyonlari[son_varyasyon_index].stok)
        elif len(urun_varyasyonlari) == 0 and int(urun.urun.stok) < istenen_adet:
            urun.adet = int(urun.urun.stok)
        else:
            urun.adet = istenen_adet

        if int(urun.adet) > 0:
            urun.save()
        elif int(urun.adet) == 0:
            urun.delete()
    return redirect('sepet')


def sepet(request, toplam=0, adet=0, sepet_urunleri=None):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))
    try:
        if request.user.is_authenticated:
            sepet_urunleri = SepetUrunu.objects.filter(kullanici=request.user, aktif=True)
        else:
            sepet = Sepet.objects.get(sepet_id=_sepet_id(request))
            sepet_urunleri = SepetUrunu.objects.filter(sepet=sepet, aktif=True)
        for sepet_urunu in sepet_urunleri:
            if sepet_urunu.urun.indirimli_fiyat:
                toplam += (sepet_urunu.urun.indirimli_fiyat * sepet_urunu.adet)
            else:
                toplam += (sepet_urunu.urun.fiyat * sepet_urunu.adet)
            for varyasyon in sepet_urunu.varyasyonlar.all():
                toplam += (varyasyon.eklenecek_fiyat * sepet_urunu.adet)
            adet += sepet_urunu.adet
    except ObjectDoesNotExist:
        pass
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
        'toplam': toplam,
        'adet': adet,
        'sepet_urunleri': sepet_urunleri
    }
    return render(request, 'magaza/sepet.html', icerik)


@login_required(login_url='giris')
def odeme(request, toplam=0, adet=0, sepet_urunleri=None):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    kargolar = Kargo.objects.all()
    adresler = Adres.objects.all().filter(kullanici=request.user)

    try:
        if request.user.is_authenticated:
            sepet_urunleri = SepetUrunu.objects.filter(kullanici=request.user, aktif=True)
        else:
            sepet = Sepet.objects.get(sepet_id=_sepet_id(request))
            sepet_urunleri = SepetUrunu.objects.filter(sepet=sepet, aktif=True)
        for sepet_urunu in sepet_urunleri:
            if sepet_urunu.urun.indirimli_fiyat:
                toplam += (sepet_urunu.urun.indirimli_fiyat * sepet_urunu.adet)
            else:
                toplam += (sepet_urunu.urun.fiyat * sepet_urunu.adet)
            for varyasyon in sepet_urunu.varyasyonlar.all():
                toplam += (varyasyon.eklenecek_fiyat * sepet_urunu.adet)
            adet += sepet_urunu.adet
    except ObjectDoesNotExist:
        pass
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
        'toplam': toplam,
        'adet': adet,
        'sepet_urunleri': sepet_urunleri,
        'kargolar': kargolar,
        'adresler': adresler
    }
    return render(request, 'magaza/odeme.html', icerik)