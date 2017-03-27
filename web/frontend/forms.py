from django import forms

class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput()
    email = forms.EmailInput()

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput()

class NewListingForm(forms.Form):
    posttitle = forms.CharField(label='Title', max_length=70)
