from django import forms
from .models import LicensePlate

class ImageForm(forms.ModelForm):

    class Meta:
        model = LicensePlate
        fields = ('image',)