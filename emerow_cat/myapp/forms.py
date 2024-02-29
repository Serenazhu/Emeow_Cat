from django import forms


class CredentialForm(forms.Form):
    email = forms.EmailField()
    key = forms.CharField()
    file = forms.FileField(label="gemini api cred.",  required=False)
