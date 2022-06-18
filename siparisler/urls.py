from django.urls import path
from . import views

urlpatterns = [
    path('siparis_ver/', views.siparis_ver, name='siparis_ver'),
    path('odemeler/', views.odemeler, name='odemeler'),
]