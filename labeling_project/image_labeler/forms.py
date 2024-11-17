from django import forms
from .models import ImageData

class ImageLabelForm(forms.ModelForm):
    class Meta:
        model = ImageData
        fields = ['label']
