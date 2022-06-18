from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
import datetime
import time

from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from kategori.models import AltKategori
from sepet.models import Sepet, SepetUrunu
from adresler.forms import AdresFormu
from ustmenu.models import UstMenu
from .models import Siparis, Odeme
from adresler.models import Adres
from kargo.models import Kargo
from hesaplar.models import Hesap
import iyzipay
import json


# Create your views here.
api_key = 'sandbox-etkBOaBAec7Zh6jLDL59Gng0xJV2o1tV'
secret_key = 'sandbox-uC9ysXfBn2syo7ZMOW2ywhYoc9z9hTHh'
base_url = 'sandbox-api.iyzipay.com'


options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}


sozlukToken = list()
conversationId = list()


@login_required(login_url='anasayfa')
def siparis_ver(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    mevcut_kullanici = request.user

    sepet_urunleri = SepetUrunu.objects.filter(kullanici=mevcut_kullanici)
    sepet_sayaci = sepet_urunleri.count()

    hatalar = []

    if sepet_sayaci <= 0:
        return redirect('magaza')

    for sepet_urunu in sepet_urunleri:
        try:
            urun = SepetUrunu.objects.get(id=sepet_urunu.id)
            istenen_adet = urun.adet
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
            hata = 'Sepete ' + urun.urun.urun_adi + ' ürününden istediğiniz seçeneklerde' + str(
                [varyasyon.varyasyon_degeri for varyasyon in urun_varyasyonlari]) + ' yalnızca ' + str(
                urun_varyasyonlari[son_varyasyon_index].stok) + ' adet ekleyebilirsiniz.'
            hatalar.append(hata)
        elif len(urun_varyasyonlari) == 0 and int(urun.urun.stok) < istenen_adet:
            urun.adet = int(urun.urun.stok)
            hata = 'Sepete ' + urun.urun.urun_adi + ' ürününden yalnızca ' + str(
                urun.urun.stok) + ' adet ekleyebilirsiniz.'
            hatalar.append(hata)

    if len(hatalar) > 0:
        hata_metni = ''
        for hata in hatalar:
            hata_metni += ' ' + hata
        icerik = {
            'ust_menu': ust_menu,
            'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
            'hata': hata_metni
        }
        return render(request, 'hata.html', icerik)

    if request.method == 'POST':
        odeme = request.POST.get('odeme')

        toplam = 0

        for sepet_urunu in sepet_urunleri:
            if sepet_urunu.urun.indirimli_fiyat:
                toplam += (sepet_urunu.urun.indirimli_fiyat * sepet_urunu.adet)
            else:
                toplam += (sepet_urunu.urun.fiyat * sepet_urunu.adet)
            for varyasyon in sepet_urunu.varyasyonlar.all():
                toplam += (varyasyon.eklenecek_fiyat * sepet_urunu.adet)

        kargo = Kargo.objects.get(takma_kargo_adi=request.POST.get('kargo'))

        if odeme != 'kredi' and odeme != 'havale' and odeme != 'kapi' and kargo is None:
            messages.error(request, 'Lütfen kargo ve ödeme yönteminizi doğru seçiniz.')
            return redirect('sepet')

        if (kargo.kapida_odeme and odeme != 'kapi') or (odeme == 'kapi' and kargo.kapida_odeme is False):
            messages.error(request, 'Lütfen kargo ve ödeme yönteminizi kapıda ödeme olarak seçiniz.')
            return redirect('sepet')

        kargosuz_toplam = toplam

        if kargo.kapida_odeme is False and toplam >= kargo.ucretsiz_kargo_limiti:
            pass
        else:
            toplam += kargo.eklenecek_fiyat

        adres = request.POST.get('address')
        data = Siparis()
        if adres == 'yeni':
            form = AdresFormu(request.POST)
            if form.is_valid():
                yeni_adres = Adres()
                yeni_adres.kullanici = mevcut_kullanici
                yeni_adres.address_title = form.cleaned_data['address_title']
                yeni_adres.first_name = form.cleaned_data['first_name']
                yeni_adres.last_name = form.cleaned_data['last_name']
                yeni_adres.phone = form.cleaned_data['phone']
                yeni_adres.email = form.cleaned_data['email']
                yeni_adres.address_line_1 = form.cleaned_data['address_line_1']
                yeni_adres.address_line_2 = form.cleaned_data['address_line_2']
                yeni_adres.country = form.cleaned_data['country']
                yeni_adres.state = form.cleaned_data['state']
                yeni_adres.city = form.cleaned_data['city']
                yeni_adres.post_code = form.cleaned_data['post_code']
                yeni_adres.save()
                mevcut_adres = Adres.objects.get(id=yeni_adres.id)
            else:
                messages.error(request, 'Lütfen adres bilginizi doğru giriniz.')
                return redirect('sepet')
        else:
            mevcut_adres = Adres.objects.get(id=adres)
        data.kullanici = mevcut_kullanici
        data.adres = mevcut_adres
        data.order_note = request.POST.get('order_note')
        data.kargo = kargo
        data.siparis_toplami = toplam
        data.ip = request.META.get('REMOTE_ADDR')
        data.save()

        yil = int(datetime.date.today().strftime('%Y'))
        ay = int(datetime.date.today().strftime('%m'))
        gün = int(datetime.date.today().strftime('%d'))
        tarih = datetime.date(yil, ay, gün)
        tarih_metni = tarih.strftime('%d%m%Y')
        siparis_numarasi = tarih_metni + str(data.id)
        data.siparis_numarasi = siparis_numarasi
        data.save()

        if odeme == 'kredi':
            buyer = {
                'id': str(mevcut_kullanici.id),
                'name': mevcut_adres.first_name,
                'surname': mevcut_adres.last_name,
                'gsmNumber': mevcut_adres.phone,
                'email': mevcut_adres.email,
                'identityNumber': '74300864791',
                'lastLoginDate': mevcut_kullanici.last_login.strftime("%Y-%m-%d %H:%M:%S"),
                'registrationDate': mevcut_kullanici.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
                'registrationAddress': mevcut_adres.address_line_1 + ' ' + mevcut_adres.address_line_2,
                'ip': str(data.ip),
                'city': mevcut_adres.city,
                'country': mevcut_adres.country,
                'zipCode': mevcut_adres.post_code
            }

            address = {
                'contactName': mevcut_adres.first_name + ' ' + mevcut_adres.last_name,
                'city': mevcut_adres.city,
                'country': mevcut_adres.country,
                'address': mevcut_adres.address_line_1 + ' ' + mevcut_adres.address_line_2,
                'zipCode': mevcut_adres.post_code
            }

            basket_items = []

            for sepet_urunu in sepet_urunleri:
                sepet_urunu_fiyat = 0
                if sepet_urunu.urun.indirimli_fiyat:
                    sepet_urunu_fiyat += (sepet_urunu.urun.indirimli_fiyat * sepet_urunu.adet)
                else:
                    sepet_urunu_fiyat += (sepet_urunu.urun.fiyat * sepet_urunu.adet)
                for varyasyon in sepet_urunu.varyasyonlar.all():
                    sepet_urunu_fiyat += (varyasyon.eklenecek_fiyat * sepet_urunu.adet)
                basket_items.append(
                    {
                        'id': str(sepet_urunu.urun.id),
                        'name': sepet_urunu.urun.urun_adi,
                        'category1': sepet_urunu.urun.kategori.kategori_adi,
                        'category2': sepet_urunu.urun.kategori.kategori_adi,
                        'itemType': 'PHYSICAL',
                        'price': str(sepet_urunu_fiyat)
                    }
                )

            request = {
                'locale': 'tr',
                'conversationId': siparis_numarasi,
                'price': str(kargosuz_toplam),
                'paidPrice': str(toplam),
                'currency': 'TRY',
                'basketId': str(data.id),
                'paymentGroup': 'PRODUCT',
                "callbackUrl": "http://localhost:8000/siparisler/odemeler/",
                "enabledInstallments": ['2', '3', '6', '9'],
                'buyer': buyer,
                'shippingAddress': address,
                'billingAddress': address,
                'basketItems': basket_items,
                # 'debitCardAllowed': True
            }

            conversationId.append(siparis_numarasi)

            checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

            content = checkout_form_initialize.read().decode('utf-8')
            json_content = json.loads(content)
            #print(json_content)
            sozlukToken.append(json_content["token"])
            return HttpResponse(json_content["checkoutFormContent"])
        elif odeme == 'havale':
            conversationId.append(siparis_numarasi)
            odeme_objesi = Odeme(
                kullanici=request.user,
                odeme_id='Havale no bekleniyor',
                odeme_sekli='havale',
                odenen_miktar=str(toplam),
                durum='Havale bekleniyor',
            )
            odeme_objesi.save()
            siparis = Siparis.objects.get(siparis_numarasi=conversationId[0])
            siparis.odeme = odeme_objesi
            siparis.siparis_verildi = True
            siparis.save()

            hata_metni = siparis_numarasi + ' numaralı siparişiniz başarıyla oluşturulmuştur. Havale bildirim ' \
                                            'formundan bize ulaştıktan sonra siparişiniz tarafınıza ' \
                                            'ulaştırılacaktır. Güzel günlerde kullanmanızı dileriz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata_metni
            }
            return render(request, 'magaza/basarili.html', icerik)
        elif odeme == 'kapi':
            conversationId.append(siparis_numarasi)
            odeme_objesi = Odeme(
                kullanici=request.user,
                odeme_id='Kapıda ödeme bekleniyor',
                odeme_sekli='kapi',
                odenen_miktar=str(toplam),
                durum='Kapıda ödeme bekleniyor',
            )
            odeme_objesi.save()
            siparis = Siparis.objects.get(siparis_numarasi=conversationId[0])
            siparis.odeme = odeme_objesi
            siparis.siparis_verildi = True
            siparis.save()

            hata_metni = siparis_numarasi + ' numaralı siparişiniz başarıyla oluşturulmuştur.' \
                                            ' Güzel günlerde kullanmanızı dileriz.'
            icerik = {
                'ust_menu': ust_menu,
                'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
                'hata': hata_metni
            }
            return render(request, 'magaza/basarili.html', icerik)
    else:
        return redirect('sepet')


@require_http_methods(['POST'])
@csrf_exempt
def odemeler(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    request_iyzico = {
        'locale': 'tr',
        'conversationId': conversationId[0],
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request_iyzico, options)
    result = checkout_form_result.read().decode('utf-8')
    sonuc = json.loads(result, object_pairs_hook=list)
    print(sonuc)
    if sonuc[0][1] == 'success':
        odeme_objesi = Odeme(
            kullanici=request.user,
            odeme_id=sonuc[7][1],
            odeme_sekli='kredi',
            odenen_miktar=sonuc[5][1],
            durum='Kart ile ödendi',
        )
        odeme_objesi.save()
        siparis = Siparis.objects.get(siparis_numarasi=conversationId[0])
        siparis.odeme = odeme_objesi
        siparis.siparis_verildi = True
        siparis.save()

        hata_metni = conversationId[0] + ' numaralı siparişiniz başarıyla oluşturulmuştur.' \
                                        ' Güzel günlerde kullanmanızı dileriz.'
        icerik = {
            'ust_menu': ust_menu,
            'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
            'hata': hata_metni
        }
        return render(request, 'magaza/basarili.html', icerik)
    else:
        hata_metni = 'Maalesef ödemeniz sırasında bir hata oluşmuştur ve siparişiniz oluşturulamamıştır. ' \
                     'Lütfen sepetinize dönüp işleminizi tekrar deneyiniz.'
        icerik = {
            'ust_menu': ust_menu,
            'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
            'hata': hata_metni
        }
        return render(request, 'magaza/basarisiz.html', icerik)