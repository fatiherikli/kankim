# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from accounts.models import DEFAULT_COLOR, UserProfile

class RegistrationForm(forms.Form):

    username = forms.RegexField(label="Kullanıcı adı", max_length=30, regex=r'^[\w.@+-]+$',
        error_messages = {'invalid': "Geçersiz karakterler kullanılmakta."})
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)
    first_name = forms.CharField(label="Adınız", max_length=30)
    last_name = forms.CharField(label="Soyadınız", max_length=30)
    email = forms.EmailField()
    color = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.initial["color"] = DEFAULT_COLOR

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu kullanıcı adı kullanılmakta.")
        return username

    def clean_email(self):
        username = self.cleaned_data.get("email")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu mail adresi kullanılmakta.")
        return username
    
    def save(self):
        kanki = User()
        kanki.username = self.cleaned_data.get("username")
        kanki.first_name = self.cleaned_data.get("first_name")
        kanki.last_name = self.cleaned_data.get("last_name")
        kanki.email = self.cleaned_data.get("email")
        kanki.is_active=True        
        password = self.cleaned_data.get("password")
        kanki.set_password(password)
        kanki.save()

        profil = kanki.get_profile()
        profil.color = self.cleaned_data.get("color")
        profil.save()

class ProfileEditForm(forms.ModelForm):

    color = forms.CharField(widget = forms.HiddenInput)

    class Meta:
        model = UserProfile
        exclude = ('user', 'picture')




class ProfilePictureForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture',)


class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Şifre", widget=forms.PasswordInput)


    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Kullanıcı adı veya şifreniz hatalı.")

        if not user.is_active:
            raise forms.ValidationError("Üyeliğiniz aktif değil.")


