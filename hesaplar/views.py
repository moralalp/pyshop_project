from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from ustmenu.models import UstMenu
from kategori.models import Kategori, AltKategori
from .forms import KayitFormu
from hesaplar.models import Hesap
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from sepet.models import Sepet, SepetUrunu
from sepet.views import _sepet_id


# Create your views here.
def uyeol(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    if request.method == 'POST':
        form = KayitFormu(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            kullanici = Hesap.objeler.create_user(first_name=first_name,
                                                  last_name=last_name,
                                                  email=email,
                                                  username=email,
                                                  password=password)
            kullanici.phone_number = phone_number
            kullanici.save()

            mevcut_site = get_current_site(request)
            mail_konu = 'Lütfen hesabınızı aktive edin'
            mesaj = render_to_string('hesaplar/hesap_aktivasyon_email.html', {
                'kullanici': kullanici,
                'alan_adi': mevcut_site,
                'uid': urlsafe_base64_encode(force_bytes(kullanici.pk)),
                'token': default_token_generator.make_token(kullanici)
            })
            gonderilen_email = email
            email_gonder = EmailMessage(mail_konu, mesaj, to=[gonderilen_email])
            email_gonder.send()

            return redirect('/hesap/giris/?komut=verifikasyon&email=' + email)
    else:
        form = KayitFormu()
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler,
        'form': form
    }
    return render(request, 'hesaplar/uyeol.html', icerik)


def aktive_et(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        kullanici = Hesap._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Hesap.DoesNotExist):
        kullanici = None
    if kullanici is not None and default_token_generator.check_token(kullanici, token):
        kullanici.is_active = True
        kullanici.save()
        messages.success(request, 'Üyeliğiniz başarılı bir şekilde aktive edildi.')
        return redirect('giris')
    else:
        messages.error(request, 'Geçersiz aktivasyon bağlantısı')
        return redirect('uyeol')


def giris(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        kullanici = auth.authenticate(email=email, password=password)
        if kullanici is not None:
            try:
                sepet = Sepet.objects.get(sepet_id=_sepet_id(request))
                sepet_bulundu = SepetUrunu.objects.filter(sepet=sepet).exists()
                if sepet_bulundu:
                    sepet_urunu = SepetUrunu.objects.filter(sepet=sepet)
                    urun_varyasyonlari = []

                    for item in sepet_urunu:
                        mevcut_varyasyonlar = item.varyasyonlar.all()
                        if mevcut_varyasyonlar is not None:
                            urun_varyasyonlari.append([list(mevcut_varyasyonlar), item.adet])
                        else:
                            urun_varyasyonlari.append([list(item.urun.takma_urun_adi), item.adet])

                    sepet_urunu = SepetUrunu.objects.filter(kullanici=kullanici)
                    eski_varyasyon_listesi = []
                    id = []

                    for item in sepet_urunu:
                        mevcut_varyasyonlar = item.varyasyonlar.all()
                        if mevcut_varyasyonlar is not None:
                            eski_varyasyon_listesi.append(list(mevcut_varyasyonlar))
                        else:
                            eski_varyasyon_listesi.append(list(item.urun.takma_urun_adi))
                        id.append(item.id)

                    for uv in urun_varyasyonlari:
                        if uv[0] in eski_varyasyon_listesi:
                            index = eski_varyasyon_listesi.index(uv[0])
                            item_id = id[index]
                            item = SepetUrunu.objects.get(id=item_id)
                            item.adet += uv[1]
                            item.kullanici = kullanici
                            item.save()
                        else:
                            sepet_urunu = SepetUrunu.objects.filter(sepet=sepet)
                            for item in sepet_urunu:
                                item.kullanici = kullanici
                                item.save()
            except:
                pass
            auth.login(request, kullanici)
            messages.success(request, 'Başarılı bir şekilde giriş yaptınız.')
            url = request.META.get('HTTP_REFERER')
            if '?next=' in url:
                sonraki_sayfa = url.rsplit('?next=')[1]
                return redirect(sonraki_sayfa)
            return redirect('panel')
        else:
            messages.error(request, 'Eksik ya da yanlış bilgi girdiniz.')
            return redirect('giris')

    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }
    return render(request, 'hesaplar/giris.html', icerik)


@login_required(login_url='giris')
def cikis(request):
    auth.logout(request)
    messages.success(request, 'Çıkış yaptınız.')
    return redirect('giris')


@login_required(login_url='giris')
def panel(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }
    return render(request, 'hesaplar/panel.html', icerik)


def sifremi_unuttum(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))
    if request.method == 'POST':
        email = request.POST.get('email')
        if Hesap.objeler.filter(email=email).exists():
            kullanici = Hesap.objeler.get(email__exact=email)
            mevcut_site = get_current_site(request)
            mail_konu = 'Şifrenizi sıfırlayın'
            mesaj = render_to_string('hesaplar/sifre_yenile_email.html', {
                'kullanici': kullanici,
                'alan_adi': mevcut_site,
                'uid': urlsafe_base64_encode(force_bytes(kullanici.pk)),
                'token': default_token_generator.make_token(kullanici)
            })
            gonderilen_email = email
            email_gonder = EmailMessage(mail_konu, mesaj, to=[gonderilen_email])
            email_gonder.send()
            messages.success(request, 'Şifrenizi yenilemeniz için email gönderilmiştir.')
            return redirect('giris')
        else:
            messages.error(request, 'Hesabınız bulunamadı.')
            return redirect('sifremi_unuttum')
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }
    return render(request, 'hesaplar/sifremi_unuttum.html', icerik)


def sifremi_unuttum_onayla(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        kullanici = Hesap._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Hesap.DoesNotExist):
        kullanici = None
    if kullanici is not None and default_token_generator.check_token(kullanici, token):
        request.session['uid'] = uid
        messages.success(request, 'Lütfen şifrenizi yenileyiniz.')
        return redirect('sifre_yenile')
    else:
        messages.error(request, 'Geçersiz şifre yenileme bağlantısı')
        return redirect('giris')


def sifre_yenile(request):
    ust_menu = UstMenu.objects.all().order_by('menu_adi')
    ust_menu_alt_kategoriler = AltKategori.objects.all().filter(ust_kategori__in=ust_menu.values_list('menu_adi'))
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            uid = request.session.get('uid')
            kullanici = Hesap.objeler.get(pk=uid)
            kullanici.set_password(password)
            kullanici.save()
            messages.success(request, 'Şifrenizi başarıyla yenilediniz.')
            return redirect('giris')
        else:
            messages.error(request, 'Girdiğiniz şifreler farklıdır.')
            return redirect('sifre_yenile')
    icerik = {
        'ust_menu': ust_menu,
        'ust_menu_alt_kategoriler': ust_menu_alt_kategoriler
    }
    return render(request, 'hesaplar/sifre_yenile.html', icerik)