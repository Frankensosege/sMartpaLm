from django import forms
from common.models import User, UserManager, Farm
class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_superuser')
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control-text'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
class AdminFarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control-text'}),
        }
        exclude = ['user_id']