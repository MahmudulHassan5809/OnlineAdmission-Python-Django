from django import forms
from django.forms import FileInput
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.EmailField(
            label=_("E-mail"), max_length=75)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'username',)


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        label='Phone Number', widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'phone_number',
                  'password1', 'password2', )
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
            # 'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            # 'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email', 'type': 'email'}),

        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].widget = forms.PasswordInput(
            attrs={'placeholder': "Password"})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'placeholder': "Confirm Password"})

        self.fields['email'].required = True
        # self.fields['first_name'].required = True
        # self.fields['last_name'].required = True
        self.fields['phone_number'].required = True


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name',)


class ProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(
        label=('Profile Pic'), required=False, widget=FileInput)

    class Meta:
        model = Profile
        fields = ('phone_number', 'address', 'profile_pic',)
