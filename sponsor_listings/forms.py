from django import forms
from .models import SponsorListingCreationModel

class SponsorListingCreationForm(forms.ModelForm):
    class Meta:
        model = SponsorListingCreationModel
        fields = '__all__' 