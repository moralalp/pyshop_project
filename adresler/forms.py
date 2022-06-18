from django import forms
from .models import Adres


class AdresFormu(forms.ModelForm):
    class Meta:
        model = Adres
        fields = ['first_name', 'last_name', 'phone', 'email', 'address_title',
                  'address_line_1', 'address_line_2', 'country', 'state', 'city', 'post_code']