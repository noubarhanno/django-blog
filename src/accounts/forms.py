from accounts.models import MyUser
from django import forms
from django.contrib.auth import authenticate,login, get_user_model
from django.contrib import messages
from .models import EmailActivation
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

class RegenerateActivationForm(forms.Form):
    email = forms.EmailField()

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super(RegenerateActivationForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg="""This Email does not exists, would you like to register? <a href='{link}'>reset your password?</a>
            """.format(link=register_link)
            # messages.success(self.request, msg, extra_tags='alert-success')
            raise forms.ValidationError(mark_safe(msg))
        return email

class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-control','id':'EmailInput'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'PasswordInput'}))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(LoginForm, self).__init__(*args, **kwargs)    

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                messages.error(self.request, "This User does not exist", extra_tags='alert-danger')
                raise forms.ValidationError("This user does not exist")
            user = authenticate(username=email, password=password)
            if not user:
                messages.error(self.request, "Incorrect password", extra_tags='alert-danger')
                raise forms.ValidationError("Incorrect passsword")
            if not user.is_active:
                messages.error(self.request, "This user is not longer active.", extra_tags='alert-danger')
                raise forms.ValidationError("This user is not longer active.")
            login(self.request,user)
            return super(LoginForm, self).clean(*args, **kwargs)

class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'Password1Input'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','id':'Password2Input'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','id':'EmailInput'}))
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','id':'NameInput'}))

    class Meta:
        model = MyUser
        fields = ('email','name')
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(RegistrationForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        qs = MyUser.objects.filter(email=email)
        if qs.exists():
            messages.error(self.request, "The email is already exist", extra_tags='alert-danger')
            raise forms.ValidationError("The email is already exist")
        if password1 and password2 and password1 != password2:
            messages.error(self.request,"Passwords are not match",extra_tags='alert-danger')
            raise forms.ValidationError("Passwords are not match")
        return password2, email
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active=False
        if commit:
            user.save()
            messages.success(self.request,"Activation email has been sent to you, please check you email to activate your account", extra_tags='alert-success')
        return user



