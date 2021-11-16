from django import forms

from phonenumber_field.formfields import PhoneNumberField

from api.models import Quote, Order, Invoice 

class UserSignUpForm(forms.Form):
    username = forms.CharField(max_length=32, required=True)
    first_name = forms.CharField(max_length=32, required=False)
    last_name = forms.CharField(max_length=32, required=False)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput(), label="Enter Password", required=True, min_length=8)
    phone = PhoneNumberField()

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=32, required=True)
    password = forms.CharField(widget=forms.PasswordInput(), label="Enter Password", required=True, min_length=8)

class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        exclude = ['user', 'created_ts', 'updated_ts']
    
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['quote', 'created_ts', 'updated_ts']
    

class InvoiceForm(forms.ModelForm):
    class Meta:
        mode = Invoice
        exclude = ['quote', 'created_ts', 'updated_ts']

