from django import forms
from accounts.models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email","phone_number","password","role"]

class LoginForm(forms.ModelForm):
   email = forms.EmailField(required=True)  
   password = forms.CharField(widget=forms.PasswordInput, required=True)         
