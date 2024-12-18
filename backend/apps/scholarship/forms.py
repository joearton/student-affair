from django import forms

class CustomForm(forms.Form):
    name = forms.CharField(label="Nama", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Pesan")