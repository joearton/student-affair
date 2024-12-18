from django import forms
from dal import autocomplete
from apps.scholarship.models import Student
from apps.worldmap.models import Province, Regency, District, Village


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'province': autocomplete.ModelSelect2(url='ac.worldmap.province'),
            'regency': autocomplete.ModelSelect2(url='ac.worldmap.regency', forward=['province']),
            'district': autocomplete.ModelSelect2(url='ac.worldmap.district', forward=['regency']),
            'village': autocomplete.ModelSelect2(url='ac.worldmap.village', forward=['district']),
        }


class CustomForm(forms.Form):
    name = forms.CharField(label="Nama", max_length=100)
    email = forms.EmailField(label="Email")
    message = forms.CharField(widget=forms.Textarea, label="Pesan")