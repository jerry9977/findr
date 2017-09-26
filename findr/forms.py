from django import forms
from .models import *


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
        exclude = ('user',)
        help_texts = {
            'username': '',
            'email': '',
            'password': '',
        }

class UserProfileForm(forms.ModelForm):
    usertype = forms.ChoiceField(choices=USERTYPES, required=True )
    
    class Meta:
        model = UserProfile
        fields = ('usertype',)
        # fields = ('website',)
		
