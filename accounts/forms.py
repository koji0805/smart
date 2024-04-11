from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model() 

class RegistForm(forms.ModelForm):
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        # このメソッドでパスワードの検証を行う
        password = self.cleaned_data.get('password')
        user = User(username=self.cleaned_data.get('username'), email=self.cleaned_data.get('email'))
        try:
            validate_password(password, user)
        except ValidationError as e:
            # パスワード検証でエラーが発生した場合は、ValidationErrorを発生させる
            raise forms.ValidationError(e.messages)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    remember = forms.BooleanField(label='ログイン状態を保持する', required=False)