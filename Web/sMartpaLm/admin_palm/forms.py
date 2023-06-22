from django import forms
from common.models import User, UserManager
class AdminUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('is_active', 'is_superuser')
        widgets = {
            'is_active': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'is_active': '사용자권한',
            'is_superuser': '관리자권한',
        }