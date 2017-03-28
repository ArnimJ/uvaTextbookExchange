from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")
    email = forms.EmailInput()
    
class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), label="Password")

class SellingForm(forms.Form):
    title = forms.CharField(max_length=70)
    
    #textbook = forms.CharField(max_length=200)
    textbookName = forms.CharField(max_length=200)
    isbn = forms.IntegerField(required=False)
    author = forms.CharField(max_length=100)
    
    c = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'))
    price = forms.DecimalField(required=True)
    condition = forms.ChoiceField(required=False, choices=c)
    details = forms.CharField(max_length=400, required=False, widget=forms.Textarea)


class BuyingForm(forms.Form):
    title = forms.CharField(max_length=70)
    
    textbookName = forms.CharField(max_length=200)
    isbn = forms.IntegerField(required=False)
    author = forms.CharField(max_length=100)
    
    c = (('New', 'New'), ('Good', 'Good'), ('Acceptable', 'Acceptable'), ('Used', 'Used'), ('Not Important', 'Not Important'))
    price = forms.DecimalField(required=True)
    condition = forms.ChoiceField( required=False, choices=c)
    details = forms.CharField(max_length=400, required=False, widget=forms.Textarea)
