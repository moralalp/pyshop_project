from django.urls import path
from . import views

urlpatterns = [
    path('uyeol/', views.uyeol, name='uyeol'),
    path('giris/', views.giris, name='giris'),
    path('cikis/', views.cikis, name='cikis'),
    path('panel/', views.panel, name='panel'),
    path('', views.panel, name='panel'),
    path('aktive_et/<uidb64>/<token>/', views.aktive_et, name='aktive_et'),
    path('sifremi_unuttum/', views.sifremi_unuttum, name='sifremi_unuttum'),
    path('sifremi_unuttum_onayla/<uidb64>/<token>/', views.sifremi_unuttum_onayla, name='sifremi_unuttum_onayla'),
    path('sifre_yenile/', views.sifre_yenile, name='sifre_yenile'),
]