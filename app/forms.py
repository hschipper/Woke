from django import forms
from app.models import Profile
 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class registration_form(UserCreationForm):
    email = forms.EmailField(
        label="Email",
        required=True
        )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user=super(registration_form,self).save(commit=False)
        user.email=self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username=forms.CharField(
        label="Username",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name':'username'
        })
    )
    password=forms.CharField(
        label="Password",
        max_length=32,
        widget=forms.PasswordInput()
    )

class MemberSearch(forms.Form):
    memberSearch = forms.CharField(
        label='State',
        max_length=30,
        widget=forms.TextInput({
            'placeholder': 'Texas'
            }))


class ProfileForm(forms.ModelForm):
    state = forms.CharField(
        label="State",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'Large-4 columns', 
            }))
    committees = forms.CharField(
        label="committee",
        max_length=100,
        widget=forms.TextInput(attrs={
            }))
    class Meta:
        model = Profile
        fields = ('state','committees')
