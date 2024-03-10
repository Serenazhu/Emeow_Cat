from django import forms
from .models import Businesses


class CredentialForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control'}))
    key = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    api = forms.FileField(label="gemini api key",  required=False,
                          widget=forms.FileInput(attrs={'class': 'form-control'}))
    # api = forms.CharField(label="gemini api key",  required=False,
    #                       widget=forms.TextInput(attrs={'class': 'form-control'}))


class TypeForm(forms.ModelForm):
    class Meta:
        model = Businesses
        fields = ['Type']
