from . import models
from django import forms
from django.contrib.auth.models import User


class CncForm(forms.ModelForm):
    class Meta:
        model = models.CncProg
        fields = ('material', 'teeth_numbers', 'cutter_diameter')

        widgets = {
            'material': forms.Select(attrs={'class': 'form-control'}),
            'teeth_numbers': forms.Select(attrs={'class': 'form-control'}),
            'cutter_diameter': forms.Select(attrs={'class': 'form-control'}),
        }


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='once again', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('password are not equal')
        return cd['password']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('birthday', 'photo')

        widgets = {
            'birthday': forms.DateTimeInput(attrs={'class': 'form-control',
                                                   'placeholder': 'year-month-day/2000-05-09'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class MyCatterForm(forms.ModelForm):
    class Meta:
        model = models.MyCutter
        fields = ('material', 'teeth_numbers', 'cutter_diameter', 'spindel_speed', 'moving_speed')

        widgets = {
            'material': forms.Select(attrs={'class': 'form-control'}),
            'teeth_numbers': forms.Select(attrs={'class': 'form-control'}),
            'cutter_diameter': forms.Select(attrs={'class': 'form-control'}),
            'spindel_speed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '6000'}),
            'moving_speed': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '800'}, ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'body')

