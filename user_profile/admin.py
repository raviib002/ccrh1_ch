"""
Project    : "CCRH"
module     : User Profile/admin
created    : 03/03/2020
Author     : Manish Kumar
"""

from django.contrib import admin
from user_profile.models import ( PractDetails,
                                  AdditionalProfile,
                                  PanelUserGroupMapping,
                           )
from django.utils.translation import ugettext, ugettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, IntegerWidget
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.formats import base_formats
from django.contrib.auth.models import User, Permission, Group
from django.forms import forms, ModelForm, Select
from import_export import resources, fields
from django.contrib.auth.admin import UserAdmin
from master.models import (State,ClinicalSetting, EmailTemplate)

from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.core.mail import send_mail,EmailMultiAlternatives,EmailMessage
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.utils.html import strip_tags, format_html
from django.contrib.auth.forms import (UserCreationForm)
from django.utils.crypto import get_random_string
from django.db.models.functions import Lower
import random
import string
from django.contrib.sites.models import Site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token

'''FINALIZED ADMIN STARTS'''
# Profile ADMIN - START 
class AdditionalProfileInline(NestedStackedInline):
    model = AdditionalProfile
    can_delete = False
    verbose_name_plural = _('Additional Profile')
    extra = 1
    max_num = 1
    fk_name = 'user'

class PractDetailsInline(NestedStackedInline):
    model = PractDetails
    can_delete = False
    verbose_name_plural = _('Practitioners Details')
    extra = 1
    max_num = 1
    fk_name = 'user'

# Customizing user creation form starts here
class UserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['groups'].required = True
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = True
        self.fields['password1'].required = False
        self.fields['password2'].required = False
        
        # If one field gets auto completed but not the other, our 'neither
        # password or both password' validation will be triggered.
        self.fields['password1'].widget.attrs['autocomplete'] = 'off'
        self.fields['password2'].widget.attrs['autocomplete'] = 'off'
        
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(u'Email %s is already in use.' % email)
    
#     def clean_first_name(self):
#         first_name = self.cleaned_data['first_name']
#         if not first_name.isalpha():
#             raise forms.ValidationError('Please enter only characterstics')
#         return first_name
#     
#     def clean_last_name(self):
#         last_name = self.cleaned_data['last_name']
#         if not last_name.isalpha():
#             raise forms.ValidationError('Please enter only characterstics')
#         return last_name
    
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(u'Username %s is already in use.' % username)
# Customizing user creation form ends here
       
class CustomUserAdmin(UserAdmin, NestedModelAdmin):
    UserAdmin.inlines = list(UserAdmin.inlines)
    UserAdmin.list_display = list(UserAdmin.list_display)
    add_form = UserCreationForm
    fieldsets = (
        (
        None,{'fields': ('groups', 'first_name', 'last_name', 'email',  'username', 'is_active', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('groups', 'first_name', 'last_name', 'email',  'username', 'is_active', ),}),
    )
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

    def __init__(self, *args, **kwargs):
        super(UserAdmin,self).__init__(*args, **kwargs)
        UserAdmin.list_display = list(UserAdmin.list_display)
        UserAdmin.actions = list(UserAdmin.actions)
        
"""After user create sending mail --starts here"""
@receiver(post_save,sender=User)
def send_mail_when_user_created_by_admin(sender, instance, **kwargs):
    try:
        user_obj = PractDetails.objects.get(user = instance).tnc
    except:
        user_obj = None
    if settings.SEND_MAIL_ALL_PLACE and  not user_obj and kwargs['created'] :
        user = User.objects.all().last()
        send_email = EmailTemplate.objects.get(email_code='CCEM004')
        subject = send_email.email_subject
        to_email = user.email
        from_email, to = settings.ADMIN_EMAIL, [to_email]
        current_site = Site.objects.get_current()
        html_content = send_email.email_body.format(
    #                                                 email_id = user.email,
    #                                                 username = user.username,
                                                    user_id = user.id,
                                                    domain= current_site.domain,
                                                    uid= urlsafe_base64_encode(force_bytes(user.id)).encode().decode(),
#                                                     token= account_activation_token.make_token(user),
                                                    scheme= 'http',
                                                    backend_reg = "br",
                                                    activate_url='/en/user/registration'
                                                )
        text_content = format_html(html_content)
        email = EmailMultiAlternatives(subject,
                                        text_content, 
                                        from_email, 
                                        to)
        email.content_subtype = 'html'
        email.send()
 
# After user create sending mail --starts here
#     @receiver(post_save,sender=PractDetails)
#     def send_mail_when_user_created_by_admin(sender, instance, **kwargs):
#         user_obj = AdditionalProfile.objects.get(user = instance.user)
#         if user_obj.profile_status.profile_status.lower() == "approved" and not kwargs['created']:
#             random_pass = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
#             if instance.user.password is not None:
#                 instance.user.set_password(random_pass)
#                 instance.user.save()
#             send_email = EmailTemplate.objects.get(email_code='CCEM001')
#             subject = send_email.email_subject
#             to_email = instance.user.email
#             from_email, to = settings.ADMIN_EMAIL, [to_email]
#             html_content = send_email.email_body.format(user_name=instance.user.first_name +' '+ instance.user.last_name,
#                                                         email_id = instance.user.email, password = random_pass,
#                                                     )
#             text_content = format_html(html_content)
#             email = EmailMultiAlternatives(subject,
#                                             text_content, 
#                                             from_email, 
#                                             to)
#             email.content_subtype = 'html'
#             email.send()
# After user create sending mail --ends here       
# Profile ADMIN - END

#PanelUserGroupMapping Admin Starts Here
class PanelUserGroupMappingResource(resources.ModelResource):
    panel_name = fields.Field(column_name=_('Panel Name'), attribute='panel_name')
    category = fields.Field(column_name=_('Category'), attribute='category')
    supervisor_pool = fields.Field(column_name=_('Supervisor Pool'), attribute='supervisor_pool')
    reviewer_pool = fields.Field(column_name=_('Reviewer Pool'), attribute='reviewer_pool')
    
    class Meta:
        model = PanelUserGroupMapping
        fields = ('panel_name','category','supervisor_pool', 'reviewer_pool')
        import_id_fields = fields
        export_order = fields
    
class PanelUserGroupMappingAdmin(ImportExportModelAdmin):
    resource_class = PanelUserGroupMappingResource
    list_display = ('panel_name','category','supervisor_pool','reviewer_pool')
    search_fields = ('panel_name','category','supervisor_pool','reviewer_pool')
    list_filter = ('panel_name','category','supervisor_pool','reviewer_pool')
#PanelUserGroupMapping Admin End Here
'''FINALIZED ADMIN ENDS'''



    
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)    
admin.site.register(PanelUserGroupMapping, PanelUserGroupMappingAdmin)