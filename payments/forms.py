from django import forms
from .models import Payment, BillingInfo, PromoCode
from .validators import (validate_cpf, validate_phone, validate_cvv,
                         validate_expiration_month, validate_expiration_year)

class BillingInfoForm(forms.ModelForm):
    cpf = forms.CharField(validators=[validate_cpf, ])
    phone = forms.CharField(validators=[validate_phone,])
    
    class Meta:
        model = BillingInfo
        fields = ['cpf', 'phone', 'address_no',
                  'address', 'postal_code']

class CreditCardForm(forms.Form):
    cc_number = forms.CharField(max_length=19)
    cvv = forms.CharField(max_length=4,
                          validators=[validate_cvv,])
    card_name = forms.CharField(max_length=30)
    expiration_month = forms.CharField(
        max_length=2,
        validators=[validate_expiration_month,]
    )
    expiration_year = forms.CharField(
        max_length=4,
        validators=[validate_expiration_year,]
    )

    def clean_expiration_year(self):
        exp_year = self.cleaned_data['expiration_year']
        if len(exp_year) == 2:
            exp_year = '20' + exp_year
        return exp_year


class PromoCodeForm(forms.Form):
    class Meta:
        model = PromoCode
        fields = ['code']


class CPFForm(forms.ModelForm):
    cpf = forms.CharField(validators=[validate_cpf, ])
    
    class Meta:
        model = BillingInfo
        fields = ['cpf',]
