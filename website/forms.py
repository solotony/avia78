from django import forms

class ContactForm(forms.Form):

    name = forms.CharField(
        required=True,
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'id':'name'})
    )

    email = forms.EmailField(
        required=True,
        label = 'Ваш e-mail',
        max_length = 100,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'id':'email'})
    )

    phone = forms.CharField(
        required=False,
        label = 'Номер телефона',
        max_length = 100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'id':'phone'})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-input', 'id':'message'}),
        required=True,
        label='текст письма',
        max_length = 10000
    )


class LoginForm(forms.Form):

    name = forms.CharField(
        required=True,
        label='Ваше имя',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input', 'id': 'name'})
    )

    email = forms.EmailField(
        required=True,
        label='Ваш e-mail',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'id': 'email'})
    )