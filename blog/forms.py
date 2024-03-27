from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django import forms
from .models import post
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
class SignUpForm(UserCreationForm):
     password1=forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
     password2=forms.CharField(label='confirm password(again)',widget=forms.PasswordInput(attrs={'class':'form-control'}))
     class Meta:
          model=User
          fields=['username','first_name','last_name','email']
          labels={'first_name':'First Name','last_name':'Last Name','email':'Email'}
          widgets={'username':forms.TextInput(attrs=
                                              {'class':'form-control'}),
          'first_name':forms.TextInput(attrs={'class':'form-control'}),
          'last_name':forms.TextInput(attrs={'class':'form-control'}),
          'email':forms.EmailInput(attrs={'class':'form-control'}),

                   }
     def clean_email(self):
                 email = self.cleaned_data['email']
                 if User.objects.filter(email=email).exists():
                        raise forms.ValidationError("This email is already exist.")
                 return email
     
     def clean_password(self):
             password = self.cleaned_data['password']
             if User.objects.filter(password=password).exists():
                        raise forms.ValidationError("This password is already exist.")
             return password
             
    
    
class LoginForm(AuthenticationForm):          
          username=UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':"form-control"}))
          password=forms.CharField(label=_('password'),strip=False,widget=forms.TextInput(attrs={'autocomplete':True,'class':"form-control"}))

class PostForm(forms.ModelForm):
       class Meta:
              model=post
              fields=['title','desc']
              labels={'title':'Title','desc':'Description'}
              widgets={'title':forms.TextInput(attrs={'class':'form-control'}),
              'desc':forms.Textarea(attrs={'class':'form-control'}),
                                            
                       }