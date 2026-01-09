import re
from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[A-Za-z0-9]+$', username):
            raise forms.ValidationError('Недопустимые символы в логине.')
        
        return username

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField()
    password2 = forms.CharField()
    class Meta:
        model = User
        fields = ['username','password']

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not re.match(r'^[A-Za-z0-9]+$', username):
            raise forms.ValidationError('Недопустимые символы в логине.')

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Логин уже занят')
        
        return username

    def clean(self):
        clean_data = super().clean()
        if clean_data.get('password') != clean_data.get('password2'):
            raise forms.ValidationError('Пароли не совпадают!')
        
        return clean_data