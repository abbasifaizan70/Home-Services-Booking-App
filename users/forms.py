# forms.py in the same Django app directory
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .mixins import AgeValidationMixin  # Import the mixin

class SignUpForm(AgeValidationMixin, UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    profile_image = forms.ImageField(
        label='Change profile image',
        required=False,
        widget=forms.FileInput
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'role', 'profile_image')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['role'].choices = [
            ('SELLER', 'Seller'),
            ('CUSTOMER', 'Customer')
        ]

class CustomUserForm(AgeValidationMixin, forms.ModelForm):
    profile_image = forms.ImageField(
        label='Change profile image',
        required=False,
        widget=forms.FileInput
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'gender', 'age', 'profile_image']
