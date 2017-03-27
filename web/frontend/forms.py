from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput()
    email = forms.EmailInput()

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.PasswordInput()

class selling(forms.Form):
    title = forms.CharField(max_length=70)
    c1 = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'))
    price = forms.DecimalField(required=True)
    condition = forms.ChoiceField(required=False)
    details = forms.CharField(max_length=400, required=False, widget=forms.Textarea)

class buying(forms.Form):
    title = forms.CharField(max_length=70)
    c1 = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'))
    price = forms.DecimalField(required=True)
    condition = forms.ChoiceField( required=False)
    details = forms.CharField(max_length=400, required=False, widget=forms.Textarea)
