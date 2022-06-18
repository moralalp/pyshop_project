from django import forms
from .models import Hesap


class KayitFormu(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Şifre'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Şifre tekrarı'
    }))

    class Meta:
        model = Hesap
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(KayitFormu, self).__init__(*args, **kwargs)
        for alan in self.fields:
            self.fields[alan].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(KayitFormu, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError(
                "Girdiğiniz şifreler aynı değildir."
            )
