from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput(label='Password')
    email = forms.EmailInput(label='Email')

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.PasswordInput(label='Password')

class selling(forms.Form):
    title = forms.CharField(label='Title', max_length=70)
    c1 = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'))
    price = forms.DecimalField(label="What price are you sell at?", required=True)
    condition = forms.ChoiceField(label= 'What is the condition of your book?', required=False)
    details = forms.CharField(label='Extra information', max_length=400, required=False)

class buying(forms.Form):
    title = forms.CharField(label='Title', max_length=70)
    c1 = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'))
    price = forms.DecimalField(label="What is your ideal price?", required=True)
    condition = forms.ChoiceField(label= 'What is the condition of your book do you want?', required=False)
    details = forms.CharField(label='Extra information?.', max_length=400, required=False)
