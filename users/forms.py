from django import forms
from .models import CreatorOrderModel, SponsorOrderModel, SupportTicket, FeatureTicket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class CreatorOrderForm(forms.ModelForm):
    class Meta:
        model = CreatorOrderModel
        fields = '__all__'

class SponsorOrderForm(forms.ModelForm):
    class Meta:
        model = SponsorOrderModel
        fields = '__all__' 

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']

class SupportTicketForm(forms.ModelForm):
    class Meta: 
        model = SupportTicket
        fields = '__all__'

class FeatureTicketForm(forms.ModelForm):
    class Meta:
        model = FeatureTicket
        fields = '__all__'