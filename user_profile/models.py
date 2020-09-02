from djongo import models
from django import forms
from django.utils.translation import ugettext_lazy as _
from audit_log.models.fields import CreatingUserField, LastUserField
from django.contrib.auth.models import User, Group
from django.db.models.deletion import CASCADE
from random import choices
from master.models import (State,City,ClinicalSetting, HospitalMaster, ClinicalSetting, CaseCategory)
from ckeditor.fields import RichTextField
from django import forms
from dal import autocomplete


'''FINALIZED MODELS STARTS'''  
#Address Additional Profile using as embedded field in AdditionalProfile Model
class AddressAdditionalProfile(models.Model):
    address_line_1 = models.TextField(blank=True, null=True,verbose_name=_("Address Line 1")) 
    address_line_2 = models.TextField(blank=True, null=True,verbose_name=_("Address Line 2"))
    pincode = models.BigIntegerField(blank=True, null=True,  verbose_name=_("Pin Code"))
    state =  models.ForeignKey(State, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("State"))
    city =  models.ForeignKey(City,  blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("City"))
    
    def __str__(self):
        return str(self.address_line_1)
    
    class Meta:
        abstract = True
        
class AddressAdditionalProfileForm(forms.ModelForm):
    address_line_1   =  forms.CharField(label=_("Address Line1"), max_length=300, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Address Line1')})) 
    address_line_2   =  forms.CharField(label=_("Address Line2"), max_length=300, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Address Line2')})) 
    pincode = forms.CharField(label=_('Pincode'),max_length='6', widget=forms.TextInput(attrs={'class':'form-control pincode', 'placeholder':_('Pincode')}))
    state=forms.ModelChoiceField(label=_("State"),
        queryset=State.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_profile:state-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'State', 'data-minimum-input-length': 2})
    )
    city=forms.ModelChoiceField(label=_("City"),
        queryset=City.objects.all(),
        widget=autocomplete.ModelSelect2(url='user_profile:city-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'City', 'data-minimum-input-length': 2})
    )
    class Meta:
            model = AddressAdditionalProfile
            fields = (
                'address_line_1', 'address_line_2','pincode','state','city'
            )

#Profile Info Additional Profile using as embedded field in AdditionalProfile Model
class ProfileInfoAdditionalProfile(models.Model):
    Profile_dis_CHOICE = ( 
        (u'0', u'No'),
        (u'1', u'Opt for Disable'),
        )
    profile_approved_datetime = models.DateTimeField(blank=True, null=True, verbose_name=("Profile Approved Date Time"))
    profile_approved_remarks = models.TextField(blank=True, null=True,verbose_name=_("Profile Approved Remarks")) 
    profile_dis_opt_by_status = models.CharField(max_length=1, default='0',choices=Profile_dis_CHOICE, verbose_name=_("Profile Disabled Opt By Status"))
    profile_dis_opt_by_remarks =  models.TextField(blank=True, null=True,verbose_name=_("Profile Disabled Opt By Remarks")) 
    profile_dis_opt_by_datetime = models.DateTimeField(blank=True, null=True, verbose_name=(" Profile Disabled Opt By Date Time"))
    profile_dis_by_remarks = models.TextField(blank=True, null=True,verbose_name=_("Profile Disabled By Remarks")) 
    profile_dis_by_datetime =  models.DateTimeField(blank=True, null=True, verbose_name=(" Profile Disabled By Date Time"))
    profile_approved_by =  models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Profile Approved By"), related_name = "ProfileApprovedBy")
    profile_dis_by= models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Profile Disabled By"), related_name = "ProfiledisBy")

    def __str__(self):
        return str(self.profile_approved_remarks)
    
    class Meta:
        abstract = True
        
class ProfileInfoAdditionalProfileForm(forms.ModelForm):
        class Meta:
            model = ProfileInfoAdditionalProfile
            fields = (
                'profile_approved_datetime', 'profile_approved_remarks','profile_dis_opt_by_status',
                'profile_dis_opt_by_remarks','profile_dis_opt_by_datetime','profile_dis_by_remarks',
                'profile_dis_by_datetime','profile_approved_by','profile_dis_by'
            )
            
#Additional Profile Model
class AdditionalProfile(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    photo = models.ImageField(upload_to='Profile_image/', default='', blank=True, null=True, verbose_name="Profile Photo")
    mobile_no = models.BigIntegerField( verbose_name=_("Mobile Number"))
    addt_mobile_no = models.BigIntegerField(blank=True, null=True, verbose_name=_("Additional Mobile Number"))
    address = models.EmbeddedField(
        model_container=AddressAdditionalProfile,
        model_form_class=AddressAdditionalProfileForm,
    )
    profile_info = models.EmbeddedField(
        model_container=ProfileInfoAdditionalProfile,
        model_form_class=ProfileInfoAdditionalProfileForm,
    )
    profile_status = models.CharField(max_length=100, blank=True, null=True, verbose_name=_(" Profile Status"))
    
    def __str__(self):
        return self.user.username+' '+self.user.email
   
    class Meta:
        verbose_name = "Additional Profile"
        verbose_name_plural = "Additional Profile"
        db_table = 'ccrh_user_addtional_profile'
#Additional Profile Table Ends here

#Creating model for  Practical Details Table Starts here
#when saving the upload path with the name starts here
def registartion_document_path_name(instance, filename):
    dir_name = instance.user.username 
    return 'Certification Upload/%s/%s' % (dir_name, filename)

#DocumentUploadPractDetails using as Array Field in PractDetails Model
class DocumentUploadPractDetails(models.Model):
    document_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Document Name"))
    document_path = models.FileField(upload_to=registartion_document_path_name, null=True, blank=True)
    
    def __str__(self):
        return self.document_name
    
    class Meta:
        abstract = True

class DocumentUploadPractDetailsForm(forms.ModelForm):
    document_name   =  forms.CharField(label=_("Document Name"), max_length=300, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('Document Name')})) 
    document_path = forms.FileField(label=_("Registration Certificate"), widget=forms.FileInput(attrs={'class':'form-control'})) 

    class Meta:
        model = DocumentUploadPractDetails 
        fields = (
            'document_name','document_path'
        )
                
#CsPractDetails using as Array Field in PractDetails Model
class CsPractDetails(models.Model):
    cs =  models.ForeignKey(ClinicalSetting, on_delete=models.CASCADE, verbose_name=_("Type Of Clinical Setting"))
    clinic_name = models.CharField(max_length=250, verbose_name=_("Clinical name"))
    clinic_id = models.CharField(max_length=250, verbose_name=_("Clinical id"))
    clinic_address_1 = models.TextField(verbose_name=_("Clinical Address 1"))
    clinic_address_2 = models.TextField(verbose_name=_("Clinical Address 2"))
    city =  models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("City"))
    state =  models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_("State"))
    pincode = models.BigIntegerField(blank=True, null=True,  verbose_name=_("Pin Code"))
    affiliation = models.CharField(blank=True, null=True,  max_length=100, verbose_name=_("Affiliation"))
    
    def __str__(self):
        return self.clinic_name
    
    class Meta:
        abstract = True


class CsPractDetailsForm(forms.ModelForm):
    cs = forms.ModelChoiceField(required=True,queryset=ClinicalSetting.objects.all(), empty_label="Select Type Of Clinical", label=_("Type Of Clinical Settings"), widget=forms.Select(attrs={'class':'form-control type_of_clinical'}))
    clinic_name = forms.CharField(required=True, label=_("Clinic / Hospital Name"), widget=forms.TextInput(attrs={'class':'form-control clinical_name','placeholder':_('Please enter 2 or more characters')}))
    clinic_id = forms.CharField(required=True, label="Clinical ID", max_length=300, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('Clinical ID')})) 
    clinic_address_1 = forms.CharField(required=True, label="Clinical/Hospital Address 1", max_length=300, widget=forms.Textarea(attrs={'class':'form-control address_1','rows':'3', 'cols':'25', 'placeholder':_('Clinical/Hospital Address 1')})) 
    clinic_address_2 = forms.CharField(required=True, label="Clinical/Hospital Address 2", max_length=300, widget=forms.Textarea(attrs={'class':'form-control adress_2','rows':'3', 'cols':'25', 'placeholder':_('Clinical/Hospital Address 2')})) 
    state = forms.ModelChoiceField(required=True, queryset=State.objects.all(), empty_label="Select State", label=_("State"), widget=forms.Select(attrs={'class':'form-control state','id':'state_id'}))
    city = forms.ModelChoiceField(required=True, queryset=City.objects.all(), empty_label="Select City", label=_("City"), widget=forms.Select(attrs={'class':'form-control city'}))
    pincode = forms.CharField(required=True, label='Pincode',max_length='6', widget=forms.TextInput(attrs={'class':'form-control pincode'}))
    affiliation  = forms.CharField(required=False, label='Affiliation',max_length='100', widget=forms.TextInput(attrs={'class':'form-control affiliation', 'placeholder':_('Affiliation')}))

    class Meta:
            model = CsPractDetails
            fields = (
                'cs','clinic_name','clinic_id','clinic_address_1' ,'clinic_address_2','city','state','pincode','affiliation',
            )
     
class PractDetails(models.Model):
    _id = models.ObjectIdField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"))
    pract_regis_body = models.CharField(max_length=10, verbose_name=_("Registration Body"))
    pract_reg_no =  models.CharField(max_length=50, verbose_name=_("Registration Number"))
    pract_state =  models.ForeignKey(State, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("State"))
    document_name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_("Document Name"))
    document_path = models.FileField(upload_to=registartion_document_path_name, verbose_name=_("Registration Document"), null=True, blank=True)

    clinical_setting = models.ArrayField(
        model_container=CsPractDetails,
        model_form_class=CsPractDetailsForm,
    )
    tnc = models.BooleanField(default=False, verbose_name=_("Terms & Conditions"))
    objects = models.DjongoManager()

    
    def __str__(self):
        return self.user.username
      
    class Meta:
        verbose_name = "Practitioner Details"
        verbose_name_plural = "Practitioner Details"
        db_table = 'ccrh_pract_details'
#Creating model for Practical Details Table Ends here

#Panel User Group Mapping Model Starts here
class Category(models.Model):
    category = models.ForeignKey(CaseCategory, on_delete=models.CASCADE, verbose_name=_("Category"))

    def __str__(self):
        return self.category.category_name
    
    class Meta:
        abstract = True

class SupervisorPool(models.Model):
    supervisor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Supervisor"))
    
    def __str__(self):
        return self.supervisor.username
    
    class Meta:
        abstract = True
        
class ReviewerPool(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Reviewer"))
    
    def __str__(self):
        return self.reviewer.username
    
    class Meta:
        abstract = True
        
class PanelUserGroupMapping(models.Model):
    _id = models.ObjectIdField()
    panel_name = models.CharField(max_length=100, verbose_name=_("Panel Name"))
    category = models.ArrayField(
        model_container=Category,
    )
    supervisor_pool = models.ArrayField(
        model_container=SupervisorPool,
    )
    reviewer_pool = models.ArrayField(
        model_container=ReviewerPool,
    )

    def __str__(self):
        return self.panel_name
    
    class Meta:
        verbose_name = "Panel User Group Mapping"
        verbose_name_plural = "Panel User Group Mapping"
        db_table = 'ccrh_panel_user_group_mapping'
#Panel User Group Mapping Model Ends here   

# #Visitor History Model Starts here
# class VisitorHistory(models.Model):
#     _id = models.ObjectIdField()
#     IS_ACCESSED_CHOICE = (
#         (u'0', u'No'),
#         (u'1', u'Yes'),
#     )
#     visitor_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("Visitor Name"))
#     visitor_email = models.CharField(max_length=100, verbose_name=_("Visitor Email"))
#     visitor_mobile = models.BigIntegerField(verbose_name=_("Visitor Mobile Number ")) 
#     visitor_datetime = models.DateTimeField( verbose_name=_("Visitor Date Time"))
#     visitor_link_unique_code = models.CharField(max_length=100, verbose_name=_("Visitor Link Unique Code"))
#     visitor_link_expiry_datetime = models.DateTimeField( verbose_name=_("Visitor Link Expiry Date Time"))
#     is_accessed = models.CharField(max_length=1, default='0',choices=IS_ACCESSED_CHOICE, verbose_name=_("Is Accessed"))
#     accessed_datetime = models.DateTimeField( verbose_name=_("Accessed Date Time"))
#     
#     class Meta:
#         verbose_name = "Visitor History"
#         verbose_name_plural = "Visitor History"
#         db_table = 'ccrh_vistor_history'
# #Visitor History Model Ends here
'''FINALIZED MODELS ENDS'''     