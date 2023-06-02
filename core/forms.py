from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    street_adress = forms.CharField(label="Dirección. Ej: Álvarez 2336")
    apartment_adress = forms.CharField(label="Departamento N°. Ej: 233 Torre A", required=False)
    country = CountryField(blank_label='(Seleccione País)').formfield(widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100',
        }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    })
    same_shipping_adress = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    save_info = forms.BooleanField(widget=forms.CheckboxInput(), required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

