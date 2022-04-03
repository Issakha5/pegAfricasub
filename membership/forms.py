from random import randint

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Value
from django.db.models.functions import Concat
from django.forms import NumberInput


class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    Address = forms.CharField()
    Hobbies = forms.CharField()
    National_ID_numbe = forms.CharField()
    Date_of_Birth = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    first_name = forms.CharField()
    last_name = forms.CharField()
    number = randint(1, 100)
    username = Concat('last_name', Value(''), 'str(number)')
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({
            'class': 'form-control',
            "name": "first_name"})
        self.fields['last_name'].widget.attrs.update({
            'class': 'form-control',
            "name": "last_name"})
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name": "username", })
        self.fields['Address'].widget.attrs.update({
            'class': 'form-control',
            "name": "Address"})
        self.fields['Date_of_Birth'].widget.attrs.update({
            'class': 'form-control',
            "name": "Date_of_Birth"})
        self.fields['Hobbies'].widget.attrs.update({
            'class': 'form-control',
            "name": "Hobbies"})
        self.fields['National_ID_numbe'].widget.attrs.update({
            'class': 'form-control',
            "name": "National_ID_numbe"})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            "name": "email"})
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            "name": "password1"})
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            "name": "password2"})