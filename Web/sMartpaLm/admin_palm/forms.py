from django import forms
class FarmCreationForm(forms.ModelForm):
    farm = forms.EmailField(
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

    # username = forms.CharField(
    #     label='사용자명',
    #     required=True,
    #     widget=forms.TextInput(
    #         attrs={
    #             'class': 'form-control',
    #             'placeholder': '사용자명',
    #             'required': 'True',
    #         }
    #     )
    # )

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
        model = ""
        fields = ("email", "password1", "password2")