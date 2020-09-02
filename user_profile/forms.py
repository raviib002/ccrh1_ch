from django.contrib.auth import authenticate
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm)

from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       UserChangeForm, PasswordResetForm, 
                                       SetPasswordForm, PasswordChangeForm)
from django import forms
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from user_profile.models import AdditionalProfile,AddressAdditionalProfile,PractDetails
from master.models import State,City,ClinicalSetting
from dal import autocomplete



class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label=_("Email or Mobile Number"), max_length=254, widget=forms.TextInput(attrs={'class':'form-control lowercase','placeholder': _('Email or Mobile Number')}))
    password = forms.CharField(required=True, label=_("Password"), widget=forms.PasswordInput(attrs={'class':'form-control','id':'password','placeholder': _('Password')}))
   
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
        return self.cleaned_data
    
"""For password reset form having email field"""
class PasswordResetFormUnique(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.TextInput(attrs={'class':'email form-control', 'placeholder':_('Email'), 'style':'text-transform:none;'}))
    def clean(self):
        cleaned_data = super(PasswordResetFormUnique, self).clean()
        email = cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email address not recognized. There is no account linked to this email."))
        return cleaned_data


"""For password reset form having passwords field"""    
class CustomPasswordChangeForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'newpassword1', 'placeholder': _('New Password')})
    )
    new_password2 = forms.CharField(
        label=_("Confirm New Password"),
        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'newpassword2', 'placeholder': _('Confirm New Password')})
    )
    old_password = forms.CharField(
        label=_("Current Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class':'form-control', 'id':'oldpassword', 'placeholder': _('Current Password')}),
    )

    field_order = ['old_password', 'new_password1', 'new_password2']
    
    
class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_("New Password"), widget=forms.PasswordInput(attrs={'class':'form-control resetpassword ','id':'newpassword1', 'placeholder': _('New Password')}))
    new_password2 = forms.CharField(label=_("Confirm New Password"), widget=forms.PasswordInput(attrs={'class':'form-control confirm-password-reset','id':'newpassword2', 'placeholder': _('Confirm New Password')}))  
    
      
        
class Addressaddprofile(forms.Form):
    address_line_1   =  forms.CharField(label="Address Line1", max_length=300, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Address Line1')})) 
    address_line_2   =  forms.CharField(label="Address Line2", max_length=300, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Address Line2')})) 
    pincode = forms.CharField(label='Pincode',max_length='6', widget=forms.TextInput(attrs={'class':'form-control pincode', 'placeholder':_('Pincode')}))
    state_name=forms.ModelChoiceField(label=_("State"),
        queryset=State.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_profile:state-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'State', 'data-minimum-input-length': 2})
    )
    city_name=forms.ModelChoiceField(label=_("City"),
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_profile:city-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'City', 'data-minimum-input-length': 2})
    )


class ClinicalSettingForm(forms.ModelForm):
    class Meta:
        model = PractDetails
        fields = ['clinical_setting']

class PractDetailsForm(forms.ModelForm):
    Choices_registration = (
        (u'', u'Select Registration Body'),
        (u'CCH', u'CCH'), 
        (u'STATE', u'STATE'),
    )
    pract_state=forms.ModelChoiceField(label=_("State"),required=False,
        queryset=State.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_profile:state-autocomplete', attrs={'class':'form-control', 'data-placeholder': 'State', 'data-minimum-input-length': 2})
    )
    pract_regis_body = forms.CharField(required=True, label='Registration Body', widget=forms.Select(choices=Choices_registration, attrs={'class':'form-control pract_regis_body'}))
    pract_reg_no = forms.CharField(label='Registration No',max_length='100', widget=forms.TextInput(attrs={'class':'form-control registration_no', 'placeholder':_('Registration No')}))
    tnc   =    forms.CharField(label=_("Terms And Conditions"), widget=forms.CheckboxInput(attrs={})) 
    
    class Meta:
        model = PractDetails
        fields = ['pract_regis_body','pract_reg_no','pract_state','tnc',]    
    
    
    
