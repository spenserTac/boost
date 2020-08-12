from django import forms
from .models import BlogListingCreationModel

class BlogListingCreationForm(forms.ModelForm):
    class Meta:
        model = BlogListingCreationModel
        fields = ['blog_url', 'niche', 'age', 'monthly_views'] 