from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput(label='Password')
    email = forms.EmailInput(label='Email')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput(label='Password')

class NewListingForm(forms.Form):
    posttitle = forms.CharField(label='Title', max_length=70)
