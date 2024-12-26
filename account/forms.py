from .models import Account, UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self): # form validation
        cleaned_data =  super().clean()
        phone = cleaned_data.get('phone_number')
  
        if len(str(phone))  != 10:
            msg = 'Phone number must be 10 digits!'
            self.add_error('phone_number', msg)

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        fields=('first_name','last_name','phone_number')
    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)  
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'  

class UserProfileForm(forms.ModelForm):
    profile_pic=forms.ImageField(required=False,error_messages={'invalid':('Image File Only')}, widget=forms.FileInput)
    class Meta:
        model=UserProfile
        fields=('address_line_1','address_line_2','city','pincode','state','country','profile_pic',)
    def __init__(self,*args,**kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)  
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'                 