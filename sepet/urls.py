from django.urls import path
from . import views

urlpatterns = [
    path('', views.sepet, name='sepet'),
    path('sepete_ekle/<int:urun_id>', views.sepete_ekle, name='sepete_ekle'),
    path('sepetten_sil/<int:urun_id>', views.sepetten_sil, name='sepetten_sil'),
    path('sepeti_guncelle', views.sepeti_guncelle, name='sepeti_guncelle'),
    path('odeme/', views.odeme, name='odeme'),
]