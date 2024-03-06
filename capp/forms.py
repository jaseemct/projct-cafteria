from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import product

# class product(forms.Form):
#     name=forms.CharFifoeld(max_length=100)
#     email=forms.EmailField(label="Email_id")
#     phone=forms.IntegerField(label="Phone NO")

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = '__all__'
    
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","email")