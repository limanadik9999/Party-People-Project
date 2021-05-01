from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponse


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Login', required=True)
    first_name = forms.CharField(label='Name', required=True)
    last_name = forms.CharField(label='Surname', required=True)
    email = forms.EmailField(required=True)

    error_messages = {
        'duplicate_username': "User with such login already exists",
        'password_mismatch': "Entered passwords are mismatched",
    }

    field_order = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        self.fields['email'].help_text = 'Please enter e-mail'
        self.fields['username'].help_text = 'Can only contain letters, numbers and symbols @ . + - _'
        self.fields['password1'].help_text = """
        The password cannot be similar to the username.

        The password must be at least 8 characters long.

        The password should not be simple and frequently used.
        
        The password should not contain only numbers.
        """
        self.fields['password2'].help_text = 'To confirm, please enter the password again.'
        self.fields['username'].widget.attrs['maxlength'] = 20
        # self.fields['username'].widget.attrs['class'] = 'w-100'
