from django import forms
from django.contrib.auth.hashers import make_password

from accounts.models import User

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','phone_number','role','address']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data['password1'])  # hash password
    #     if commit:
    #         user.save()
    #     return user
    def save(self, commit=True):
        user = super().save(commit=False)

        user.password = make_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class EmailLoginForm(forms.Form):
   # email = forms.EmailField()
   username = forms.CharField()
   password = forms.CharField(widget=forms.PasswordInput)