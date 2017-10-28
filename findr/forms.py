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
            'name': '',
            'username': '',
            'email': '',
            'password': '',
        }

class UserProfileForm(forms.ModelForm):
    name = forms.CharField(required=True)
    usertype = forms.ChoiceField(choices=USERTYPES, required=True )
    phoneNumber = forms.CharField()
    address = forms.CharField()
    
    class Meta:
        model = UserProfile
        fields = ('name', 'phoneNumber', 'address', 'usertype')
 
        

