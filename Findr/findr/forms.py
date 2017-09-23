from findr.models import UserProfile
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

USERTYPES = (
    ('1', 'Student'),
    ('2', 'Tourist'),
    ('3', 'Businessman'),
)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    usertype = forms.ChoiceField(choices=USERTYPES, required=True )
    
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')
