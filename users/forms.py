from django import forms
from .models import CreatorOrderModel, SponsorOrderModel

class CreatorOrderForm(forms.ModelForm):
    class Meta:
        model = CreatorOrderModel
        fields = '__all__'

class SponsorOrderForm(forms.ModelForm):
    class Meta:
        model = SponsorOrderModel
        fields = '__all__' 