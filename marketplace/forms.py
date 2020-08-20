from django import forms
from users.models import UserWatchDashboardModel

class UserWatchDashboardForm(forms.ModelForm):
    class Meta:
        model = UserWatchDashboardModel
        fields = ['watched_creator', 'user'] 