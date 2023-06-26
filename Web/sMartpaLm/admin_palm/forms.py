from django import forms
from common.models import User, UserManager
class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_superuser')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control-text'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
