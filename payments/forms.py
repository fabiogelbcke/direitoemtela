from django import forms
from .models ipmort Payment, BillingInfo
from .validators import validate_cpf, validate_phone

class BillingInfoForm(models.ModelForm):
    cpf = forms.CharField(validators=[validate_cpf, ])
    phone = forms.CharField(validators=[validate_phone,])
    
    class Meta:
        model = BillingInfo
        fields = ['cpf', 'phone']

class CreditCardForm(forms.Form):
    cc_number = forms.CharField(max_length=19,
                                validators=[validate_cc,])
    cvv = forms.CharField(max_length=4,
                          validators=[validate_cvv,])
    card_name = forms.CharField(max_length=30)
    expiration_date = forms.CharField(
        max_length=5,
        validators=[validate_expiration_date,]
    )
