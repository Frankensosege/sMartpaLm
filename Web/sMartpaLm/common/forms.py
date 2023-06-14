from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm
from .models import User, UserManager

# class UserForm(forms.ModelForm):
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'user_name', 'password']
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'user_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': '이메일',
            'user_name': '표시명',
            'password': '비밀번호',
        }
# class UsrCreationForm(UserCreationForm):
class UserCreationForm(forms.ModelForm):
    email = forms.EmailField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': '이메일 주소',
                'required': 'True',
            }
        )
    )
    user_name = forms.CharField(
        label='사용자명',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '사용자명',
                'required': 'True',
            }
        )
    )

    password1 = forms.CharField(
        label='비밀번호',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호',
                'required': 'True',
            }
        )
    )
    password2 = forms.CharField(
        label='비밀번호 확인',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': '비밀번호 확인',
                'required': 'True',
            }
        )
    )
    class Meta:
        model = User
        fields = ("user_name", "password1", "password2", "email")

    def clean_password2(self):
        # 두 비밀번호 입력 일치 확인
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.email = UserManager.normalize_email(self.cleaned_data['email'])
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label='비밀번호'
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'user_name', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]