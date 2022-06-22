from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import *


def ForbiddenUsers(value):
    forbidden_users = ['admin', 'css', 'js', 'authenticate', 'login', 'logout', 'administrator', 'root',
	'email', 'user', 'join', 'sql', 'static', 'python', 'delete']
    if value.lower() in forbidden_users:
        raise ValidationError('Invalid name for user, this is a reserverd word.')

def InvalidUser(value):
	if '@' in value or '+' in value or '-' in value:
		raise ValidationError('This is an Invalid user, Do not user these chars: @ , - , + ')

def UniqueEmail(value):
	if User.objects.filter(email__iexact=value).exists():
		raise ValidationError('User with this email already exists.')

def UniqueUser(value):
	if User.objects.filter(username__iexact=value).exists():
		raise ValidationError('User with this username already exists.')



class SignupForm(UserCreationForm):    
    username = forms.CharField(max_length=20)
    email = forms.EmailField(max_length=200, help_text='Required. Please enter a valid email address.')
    password1 = forms.CharField(max_length=20)
    password2 = forms.CharField(max_length=20)
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
        def __init__(self, *args, **kwargs):
            super(SignupForm, self).__init__(*args, **kwargs)
            self.fields['username'].validators.append(ForbiddenUsers)
            self.fields['username'].validators.append(InvalidUser)
            self.fields['username'].validators.append(UniqueUser)
            self.fields['email'].validators.append(UniqueEmail)
  
        def clean(self):
            super(SignupForm, self).clean()
            password1 = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('confirm_password')
            
            if password1 != password2:
                self._errors['password'] = self.error_class(['Passwords do not match. Try again'])
                return self.cleaned_data
            
class LoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password1')  
        
        
class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class': 'input is-medium'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class': 'input is-medium'}), required=True)
    
    class Meta:
        model = Post
        fields = ('content', 'caption', 'tags')
		
		
  
class CommentForm(forms.ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea'}), required=True)
     
    class Meta:
        model = Comment
        fields = ('body',)