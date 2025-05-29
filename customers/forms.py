from django import forms
from django.contrib.auth.hashers import make_password

from accounts.models import User

class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','phone_number','role','address','store']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # If not logged in: only allow customer or store_admin
        if not self.request or not self.request.user.is_authenticated:
            self.fields['role'].choices = [
                ('customer', 'customer'),
                ('admin', 'admin'),
            ]
            # For registration, store can be empty
            self.fields['store'].required = False
        else:
            user = self.request.user
            if user.role == 'admin':
                self.fields['role'].choices = [
                    ('manager', 'manager'),
                    ('operator', 'operator'),
                ]
            else:
                pass

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

class OTPPhoneForm(forms.Form):
    phone = forms.CharField(max_length=11,label='phone number')

class OTPCodeForm(forms.Form):
    otp = forms.CharField(max_length=4, label='received code')

class StaffForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email','phone_number','role','address']

