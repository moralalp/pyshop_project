"""pyshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.magaza, name='magaza'),
    path('<slug:takma_kategori_adi>', views.magaza, name='kategoriye_gore_urunler'),
    path('<slug:takma_kategori_adi>/<slug:takma_alt_kategori_adi>', views.magaza, name='alt_kategoriye_gore_urunler'),
    path('<slug:takma_kategori_adi>/urun/<slug:takma_urun_adi>', views.urun_detayi, name='kategoriye_gore_urun_detayi'),
    path('<slug:takma_kategori_adi>/<slug:takma_alt_kategori_adi>/urun/<slug:takma_urun_adi>', views.urun_detayi, name='alt_kategoriye_gore_urun_detayi'),
]
