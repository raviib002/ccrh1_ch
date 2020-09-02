import json
import random
import re
import string
import requests
import os
import datetime
from django.contrib.auth import views as auth_views
from django.db import connection
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from user_profile.forms import LoginForm, PasswordResetFormUnique
from django.http import HttpResponseRedirect, HttpResponse, response
from django.urls.base import reverse_lazy
from django.conf import settings
from user_profile.forms import (PractDetailsForm, CustomPasswordChangeForm, ClinicalSettingForm, Addressaddprofile)
from django.contrib.auth import views as auth_views
from django.core.mail import (send_mail,
                              EmailMultiAlternatives,
                              EmailMessage
                              )
from django.utils.html import strip_tags, format_html
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.translation import ugettext as _
from utils.common_functions import (make_unique_username)
from notifications.signals import notify

from master.models import (State, City, ClinicalSetting,HospitalMaster, EmailTemplate, CaseCategory)
from wsgiref.util import FileWrapper
import mimetypes
from django.utils.encoding import smart_str
from notifications.models import Notification
from notifications.views import mark_as_read
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (api_view,
                                       parser_classes,
                                       permission_classes,
                                       renderer_classes
                                       )
from django.db.models.functions import Lower
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.sites.models import Site
import base64
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time
# from user_profile.views import user_profile_views
from django.template import loader
from rest_framework import parsers, renderers, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.views import APIView
from user_profile.models import (AdditionalProfile, AddressAdditionalProfile,
                                 ProfileInfoAdditionalProfile, DocumentUploadPractDetails,
                                 PractDetails, DocumentUploadPractDetails, CsPractDetails,
                                 AddressAdditionalProfileForm, CsPractDetailsForm,
                                 Category, SupervisorPool, ReviewerPool, PanelUserGroupMapping
)
from dal import autocomplete
from django.forms.models import model_to_dict
from bson import json_util, ObjectId
from django.db.models import Q
from django.core.paginator import Paginator
from case_history.models import CaseRepertorisation


"""Case History Check User Existence Functionality - starts"""
@csrf_exempt
@parser_classes([JSONParser])
@api_view(['POST'])
def check_user_api(request):
    if request.method == "POST":
        data = request.data #Getting the parameters
        if data.get('username') and data.get('password'):
            user = authenticate(username=data.get('username'),
                                password=data.get('password')
                                )
        if user is not None:
            if user.is_active:
                results = {'status':1,
                           'message':user.id,
                         }
            else:
                message = _('Account is Blocked ! Please contact Admin')
                results = {'status':0,
                           'message':message,
                         }
            return Response(results)
"""Case History Check User Existence Functionality - ends"""

# """Case History Check User Existence Functionality - starts"""
# @csrf_exempt
# @parser_classes([JSONParser])
# @api_view(['POST'])
# def check_user_forgot_api(request):
#     data = request.data #Getting the parameters
# #     user_dtl = User.objects.filter(email=data.get('user_email')).exists()
# #     if user_dtl:
# #         data = {'status':'success'}
# #     else:
# #         data = {'status':'error'},
# #     return Response(data)
# """Case History Check User Existence Functionality - ends"""

"""sending an email Starts here"""
class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        """
          Handles password reset tokens
          When a token is created, an e-mail needs to be sent to the user
        """
        subject = 'CCRH Password Reset'
        # Email subject *must not* contain newlines
        current_site = Site.objects.get_current()
        context = {
            'user':reset_password_token.user,
            'reset_password_url': "{}/reset-password/{}".format(settings.FORGOT_PASSWORD_URL, reset_password_token.key),
            'uid':reset_password_token.key,
            'domain': current_site.domain
        }
        message = loader.render_to_string('user_profile/password_reset_email.html', context)
        email = EmailMessage(subject, message, to=[reset_password_token.user.email])
        email.content_subtype = 'html'
        email.send()

"""After click on link updating the password"""
class CustomPasswordTokenVerificationView(APIView):
    """
      An Api View which provides a method to verifiy that a given pw-reset token is valid before actually confirming the
      reset.
    """
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    def post(self, request, *args, **kwargs):
        try:
            token = request.data.get('token')
        except:
            token = None
#         token = serializer.validated_data['token']
        password = request.data.get('password')
        # get token validation time
#         password_reset_token_validation_time = get_password_reset_token_expiry_time()
        # find token
        try:
            reset_password_token = ResetPasswordToken.objects.get(key=token)
        except:
            reset_password_token = None
        if password:
            user = User.objects.get(id=reset_password_token.user_id)
            user.set_password(password)
            user.save()
            reset_password_token.delete()
        else:
            if reset_password_token is None:
                return Response({'status': 'expired'}, status=status.HTTP_404_NOT_FOUND)
        if not reset_password_token.user.has_usable_password():
                return Response({'status': 'irrelevant'})
        return Response({'status': 'OK'})

"""Case History Login Functionality - starts"""
@csrf_exempt
def login_view(request):
    ccrh_login = settings.CCRH_LOGIN_URL
    if request.method == 'GET':
        return HttpResponseRedirect(ccrh_login)
    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        user=authenticate(username=username,password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser or user.is_staff:
                    return HttpResponseRedirect('/admin/')
                else:
                    return HttpResponseRedirect(reverse_lazy('case_history:dashboard'))
        return HttpResponseRedirect(ccrh_login)
"""Case History Login Functionality - ends"""
"""CCRH Logout Functionality - starts"""
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)
"""CCRH Logout Functionality - ends"""


"""Forgot Password functionality. - Starts"""
def password_forgot(request):
    fp_form = PasswordResetFormUnique()
    success = request.session.pop('success_msg', None)
    #To show invalid email error message - starts
    old_post = request.session.pop('_old_post', None)
    if old_post:
        fp_form = PasswordResetFormUnique(old_post)

    if request.method == 'GET':
        form = PasswordResetFormUnique()
        return render(request, 'user_profile/forget_password.html',{'form':form,
                                                                    'fpform':fp_form,
                                                                    'old_post':old_post,
                                                                    'success_msg':success,
                                                                    })

    elif request.method == 'POST':
        form = PasswordResetFormUnique(request.POST)
        if form.is_valid():
            request.session['success_msg'] = _('We have sent a link to change your password. Kindly check your Email.')
            return auth_views.PasswordResetView.as_view(
                            form_class = PasswordResetFormUnique,
                            template_name = 'user_profile/forget_password.html',
                            email_template_name = 'user_profile/password_reset_email.html',
                            success_url = reverse_lazy('user_profile:forget_password'),
                            )(request)
        else:
            request.session['_old_post'] = request.POST
            return HttpResponseRedirect(reverse_lazy('user_profile:forget_password'))
            return render (request, 'user_profile/forget_password.html',{'form':form,
                                                                         'fpform':fp_form,
                                                                         })
    else:
        return HttpResponseRedirect(reverse_lazy('user_profile:forget_password'))
"""Forgot Password functionality. - Ends"""


"""Change Password functionality. - Starts"""
@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            success= _('Password has been changed successfully.')
            return render(request, 'user_profile/password_change.html', {'form': form,
                                                                         'note':success})
        else:
            return render(request, 'user_profile/password_change.html', {'form': form })
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'user_profile/password_change.html', {'form': form })

"""Change Password functionality. - Ends"""


"""Registration Step1 Function Starts here"""
def registration_profile_info(request, uidb64=None, br=None):
    if request.method == "GET":
        additional_details  = additional_form = user_confirmation=user_obj  =None
        city_name = City.objects.filter().values_list('_id','city_name')
        state = State.objects.filter().values_list('_id','state_name')
        """In the url passing front end registration"""
        if not br:
            br = "fr"
        
        """In the url fetching user id in encrypted converting to int"""
       
        if uidb64:
            try:
                uid = force_text(urlsafe_base64_decode(uidb64))
                user_confirmation = User.objects.get(id=uid)
            except(TypeError, ValueError, OverflowError, User.DoesNotExist):
                user_confirmation = None
        """Before 24 hours user wants to update user profile checking the condition user presentd or not"""
        try:
            additional_details_exist = AdditionalProfile.objects.get(user=user_confirmation.id)
        except:
            additional_details_exist =  None
        if  additional_details_exist:
            try:
                additional_details = AdditionalProfile.objects.get(_id=additional_details_exist._id)
            except:
                additional_details =  None
            additional_form = AddressAdditionalProfileForm(instance=additional_details.address)
        else:
            additional_form = AddressAdditionalProfileForm()
        if user_confirmation:
            try:
                user_obj = User.objects.get(id=user_confirmation.id)
            except:
                user_obj = None
        return render(request, 'user_profile/registration_profile_info.html',{
                                                                                    #'form':form,
                                                                                    'state_obj':state,
                                                                                    'city_name':city_name,
                                                                                    'additional_details':additional_details,
                                                                                    'additional_form':additional_form,
                                                                                     'user_obj':user_obj,         
                                                                                     'backend_reg':br,                                                                   
                                                                                     })

    elif request.method == "POST":
    #Generating random password here
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
    #   Adding Data in user table
        '''If user already register first step and start register from first step again --starts'''
        exist_user_id = None
        if User.objects.filter(email=request.POST.get('email')).exists():
            exist_user = User.objects.get(email=request.POST.get('email'))
            exist_user_id = exist_user.id
        elif AdditionalProfile.objects.filter(mobile_no=request.POST.get('mobile_no')).exists():
            exist_user = AdditionalProfile.objects.get(mobile_no=request.POST.get('mobile_no'))
            exist_user_id = exist_user.user_id
        
        '''If user already register first step and start register from first step again --ends'''
        if request.POST.get('user_id') and not User.objects.filter(email=request.POST.get('email')).exclude(id=request.POST.get('user_id')).exists() and not AdditionalProfile.objects.filter(mobile_no=request.POST.get('mobile_no')).exclude(user=request.POST.get('user_id')).exists():
            user_id = User.objects.filter(id=request.POST.get('user_id')).update(first_name=request.POST.get('first_name'),
                                        last_name = request.POST.get('last_name'),
                                        email = request.POST.get('email'),
                                        is_active = 0,
                                        )
            try:
                backen_user_id = AdditionalProfile.objects.get(user=request.POST.get('user_id'))
            except:
                backen_user_id = None
            if request.POST.get('backend_registration') and not backen_user_id:
                additiona_prf = AdditionalProfile.objects.create(user_id = request.POST.get('user_id'),
                                                mobile_no = request.POST.get('mobile_no'),
                                                address = AddressAdditionalProfile(
                                                        address_line_1 = request.POST.get('address_line_1'),
                                                        address_line_2 = request.POST.get('address_line_2'),
                                                        pincode = request.POST.get('pincode'),
                                                        state = State.objects.get(_id=request.POST.get('state')),
                                                        city = City.objects.get(_id=request.POST.get('city')),
                                                        ),
                                                profile_info = ProfileInfoAdditionalProfile(),
                                                profile_status = "Pending for Approval"
                                                )
            else:
                try:
                    additiona_prf = AdditionalProfile.objects.get(user_id=request.POST.get('user_id'))
                except:
                    additiona_prf = None
                if additiona_prf:
                    additiona_prf.mobile_no = request.POST.get('mobile_no')
                    additiona_prf.address = AddressAdditionalProfile(
                                address_line_1 = request.POST.get('address_line_1'),
                                address_line_2 = request.POST.get('address_line_2'),
                                pincode = request.POST.get('pincode'),
                                state = State.objects.get(_id=request.POST.get('state')),
                                city = City.objects.get(_id=request.POST.get('city')),
                                )
                    additiona_prf.save()
            return HttpResponseRedirect(reverse_lazy('user_profile:documentation_upload',  kwargs={'user_id':urlsafe_base64_encode(force_bytes(request.POST.get('user_id'))),
                                                                                                   'br':request.POST.get('backend_reg')}))
        elif (User.objects.filter(email=request.POST.get('email')).exists() or AdditionalProfile.objects.filter(mobile_no=request.POST.get('mobile_no')).exists()) and  not PractDetails.objects.filter(tnc=True, user_id=exist_user_id).exists():
            user_id = User.objects.filter(id=exist_user_id).update(first_name=request.POST.get('first_name'),
                                        last_name = request.POST.get('last_name'),
                                        email = request.POST.get('email'),
                                        )
            try:
                additiona_prf = AdditionalProfile.objects.get(user_id=exist_user_id)
            except:
                additiona_prf = None
            if additiona_prf:
                additiona_prf.mobile_no = request.POST.get('mobile_no')
                additiona_prf.address = AddressAdditionalProfile(
                            address_line_1 = request.POST.get('address_line_1'),
                            address_line_2 = request.POST.get('address_line_2'),
                            pincode = request.POST.get('pincode'),
                            state = State.objects.get(_id=request.POST.get('state')),
                            city = City.objects.get(_id=request.POST.get('city')),
                            )
                additiona_prf.save()
                
            return HttpResponseRedirect(reverse_lazy('user_profile:documentation_upload',  kwargs={'user_id':urlsafe_base64_encode(force_bytes(exist_user_id)),
                                                                                                   'br':request.POST.get('backend_reg')}))
        elif not User.objects.filter(email=request.POST.get('email')).exists() and not AdditionalProfile.objects.filter(mobile_no=request.POST.get('mobile_no')).exists():
            user_id = User.objects.create_user(first_name=request.POST.get('first_name'),
                                          last_name = request.POST.get('last_name'),
                                          email = request.POST.get('email'),
                                          username = make_unique_username(request.POST.get('email')),
                                          is_active = 0,
                                          password =random_string)
            #creating Additional Profile starts here
            additiona_prf = AdditionalProfile.objects.create(user = user_id,
                                                mobile_no = request.POST.get('mobile_no'),
                                                address = AddressAdditionalProfile(
                                                        address_line_1 = request.POST.get('address_line_1'),
                                                        address_line_2 = request.POST.get('address_line_2'),
                                                        pincode = request.POST.get('pincode'),
                                                        state = State.objects.get(_id=request.POST.get('state')),
                                                        city = City.objects.get(_id=request.POST.get('city')),
                                                        ),
                                                profile_info = ProfileInfoAdditionalProfile(),
                                                profile_status = "Pending for Approval"
                                                )
            return HttpResponseRedirect(reverse_lazy('user_profile:documentation_upload',  kwargs={'user_id':urlsafe_base64_encode(force_bytes(additiona_prf.user_id)),
                                                                                                   'br':request.POST.get('backend_reg')}))
        else:
            already_exists=_('Mobile Number or Email already Exists')
            try:
                additional_form = AddressAdditionalProfileForm(request.POST)
            except:
                additional_form = AddressAdditionalProfileForm()
            return render(request, "user_profile/registration_profile_info.html",{'first_name':request.POST.get('first_name'),
                                                                                'additional_form':additional_form,
                                                                                'last_name':request.POST.get('last_name'),
                                                                                'email':request.POST.get('email'),
                                                                                'mobile_no' : request.POST.get('mobile_no'),
                                                                                'message':already_exists,
                                                                                'backend_reg':request.POST.get('backend_reg'),  
                                                                          })

"""Registration Step2 Function Starts here"""
def registration_document_upload(request, user_id=None, br=None):
    if request.method == "GET":
        encryp_user_id = None
        tnc_url = settings.CCRH_HOME_URL
        registration_success = request.session.pop('registration_success', None)
        if br == 'br':
            group_obj = Group.objects.all() 
        else:
            group_obj = Group.objects.filter(id__in=[1, 2, 3, 4])
        clinical_setting = ClinicalSetting.objects.filter().values_list('_id','cs_name')
        try:
            uid = force_text(urlsafe_base64_decode(user_id))
            user_id = User.objects.get(id=uid).id
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user_id = None
        try:
            pract = PractDetails.objects.get(user_id=user_id)
        except:
            pract = None
        pract_form=PractDetailsForm(instance = pract)
        try:
            pract_detail = PractDetails.objects.filter(user_id=user_id).last()
        except:
            pract_detail = None
        try:
            aditional_profil  = AdditionalProfile.objects.get(user_id=user_id)
        except:
            aditional_profil = None
        if aditional_profil:
            backend_group = aditional_profil.user.groups.values_list('id',flat = True)
        else:
            backend_group = []
        """populating userprofile data convertig userid to cncrypt"""
        if aditional_profil:
            encryp_user_id = urlsafe_base64_encode(force_bytes(aditional_profil.user_id))
        return render(request, 'user_profile/registration_document_upload.html',{'pract_form':pract_form,
                                                                                'group_obj':group_obj,
                                                                                'clinical_setting':clinical_setting,
                                                                                'user_id':user_id,
                                                                                'pract_detail':pract_detail,
                                                                                'tnc_url':tnc_url,
                                                                                'pract':pract,
                                                                                'registration_success':registration_success,
                                                                                'aditional_profil':aditional_profil,
                                                                                'backend_group':backend_group,
                                                                                'encryp_user_id':encryp_user_id,
                                                                                'backend_reg':br,   
                                                                                })   
    if request.method == "POST":
        form = PractDetailsForm(request.POST)
        if form.is_valid():
            data = {k: v for k, v in form.cleaned_data.items()}
            #saving the practical details
            if PractDetails.objects.filter(user_id = request.POST.get('user')):
                practitioner = PractDetails.objects.filter(user_id=request.POST.get('user')).update(
                                            **data)
            if practitioner:
                pract_details = PractDetails.objects.get(user_id = request.POST.get('user'))
            else:
                pract_details = None
            '''inserting an image in additional profile --starts here'''
            '''inserting an certificate in practitioner details --starts here'''
            register_certificate = request.FILES.get('document_path')
            if register_certificate:
                pract_details.document_path = register_certificate
                pract_details.save()
                '''inserting an certificate in practitioner details --ends here'''
            image_data = request.FILES.get('upload_photo', None)
            if image_data:
                additional_prf = AdditionalProfile.objects.get(user_id = request.POST.get('user'))
                additional_prf.photo = image_data
                additional_prf.save()
            '''inserting an image in additional profile --ends here'''
            
            '''inserting an user to group --starts here'''
            try:
                user_id = User.objects.get(id=request.POST.get('user'))
            except:
                user_id = None
            try:
                user_id.groups.add(request.POST.get('group_id'))
            except:
                pass
            '''inserting an user to group --ends here'''
            
            '''Sending an email verification to the user starts here'''
            if settings.SEND_MAIL_ALL_PLACE:
                send_email = EmailTemplate.objects.get(email_code='CCEM003')
                subject = send_email.email_subject
                to_email = pract_details.user.email
                from_email, to = settings.ADMIN_EMAIL, [to_email]
                current_site = get_current_site(request)
                html_content = send_email.email_body.format(user = pract_details.user.first_name +' '+ pract_details.user.last_name,
                                                            domain= current_site.domain,
                                                            uid= urlsafe_base64_encode(force_bytes(pract_details.user.id)).encode().decode(),
                                                            token= account_activation_token.make_token(pract_details.user),
                                                            scheme= 'https' if request.is_secure() else 'http',
                                                            activaion_url='/en/user/activate')
                text_content = format_html(html_content)
                email = EmailMultiAlternatives(subject,
                                                text_content,
                                                from_email,
                                                to)
                email.content_subtype = 'html'
                email.send()
            '''Sending an email verification to the user ends here'''
                 
            content = "Registration Approval"
            if settings.SEND_NOTIFICATIONS_ALL_PLACE:
                notify.send(pract_details.user,
                            recipient=User.objects.filter(email=settings.ADMIN_REGISTRATION_EMAIL),
                            verb='New Registration Form',
                            description=content,
                            level='Newly Registered')
            request.session.pop('user_id', None)
            request.session['registration_success'] = _("Your account has been created successfully. Kindly check your inbox and verify email.")
            return HttpResponseRedirect(reverse_lazy('user_profile:documentation_upload',  kwargs={'user_id':urlsafe_base64_encode(force_bytes(request.POST.get('user'))),
                                                                                                    'br':request.POST.get('backend_reg')}))
            
        else:
            pract_form = PractDetailsForm()
            return render(request, 'user_profile/registration_document_upload.html',{'pract_form':pract_form,
                                                                                })                                                 


"""Clinical Setting ADD, Update, Delete Functionality --Starts Here"""
def clinical_settings_data(request):
    if request.method == "POST":
        user_json = {}
        try:
            city = City.objects.get(city_name=request.POST.get('city_name'))
            state = State.objects.get(state_name=request.POST.get('state_name'))
        except:
            state = None
            city = None
        
        if HospitalMaster.objects.filter(hospital_name=request.POST.get('clinic_name')):
            pass
        else:
            HospitalMaster.objects.create(hospital_name = request.POST.get('clinic_name'),
                                          hospital_type = ClinicalSetting.objects.get(_id=request.POST.get('type_of_clinical')),
                                          address_1 = request.POST.get('address_1'),
                                          address_2 = request.POST.get('address_2'),
                                          city_id=city._id,
                                          state_id=state._id,
                                          pincode = request.POST.get('pincode'))
            
        
        try:
            pract = PractDetails.objects.get(user_id=request.POST.get('user'))
        except:
            pract = None
            
        try:
            hospital_mastr = HospitalMaster.objects.get(hospital_name=request.POST.get('clinic_name'))
        except:
            hospital_mastr = None
        
        a_list = [CsPractDetails(cs=ClinicalSetting.objects.get(_id=request.POST.get('type_of_clinical')),
                                 clinic_id = hospital_mastr._id,
                                 clinic_name=hospital_mastr.hospital_name,
                                 clinic_address_1=request.POST.get('address_1'),
                                 clinic_address_2=request.POST.get('address_2'),
                                 state_id=state._id,
                                 city_id=city._id,
                                 pincode=request.POST.get('pincode'),
                                 )]
        
        if not request.POST.get('edit_clinical') and pract:
            pract.clinical_setting.extend(a_list)
            pract.save()
            user_json['success'] = _('Clinical Setting Add Successfully')
#             
        elif request.POST.get('edit_clinical'):
            pract_details = PractDetails.objects.get(user_id=request.POST.get('user_id'), clinical_setting={'clinic_id':request.POST.get('edit_id')})
            pract_details.clinical_setting.pop(int(request.POST.get('index_no'))-1)
            pract_details.clinical_setting.extend(a_list)
            pract_details.save()
            user_json['success'] = _('Clinical Setting Updated Successfully')
        else: 
            pract_details = PractDetails.objects.create(user_id = request.POST.get('user'),
                                pract_regis_body = request.POST.get('pract_regis_body'),
                                pract_reg_no = request.POST.get('pract_reg_no'),
                                pract_state_id = request.POST.get('pract_state'),
                                document_name=request.POST.get('document_name'),
                                document_path=request.FILES.get('document_path'),
                            clinical_setting = a_list)
            
            '''inserting an image in additional profile --starts here'''
            image_data = request.FILES.get('upload_photo', None)
            if image_data:
                additional_prf = AdditionalProfile.objects.get(user_id = request.POST.get('user', None))
                additional_prf.photo = image_data
                additional_prf.save()
            '''inserting an image in additional profile --ends here'''
             
            '''inserting an user to group --starts here'''
            try:
                user_id = User.objects.get(id=request.POST.get('user', None))
            except:
                user_id = None
            if request.POST.get('group_id'):
                user_id.groups.add(request.POST.get('group_id'))
            '''inserting an user to group --ends here'''
            if pract_details:
                user_json['success'] = _('Clinical Setting Add Successfully')
            else:
                user_json['success'] = _('Failed, Clinical Setting Add.Please Try Again')
         
        return JsonResponse(user_json)
        
def clinical_setting_data_edit(request, edit_id=None, index=None):
    if request.method == "GET":
        pract_details = PractDetails.objects.get(clinical_setting={'clinic_id':edit_id}, user_id=request.GET.get('user_id'))
        pract_detail = pract_details.clinical_setting[index-1]
        clinical_setting = ClinicalSetting.objects.filter().values_list('_id','cs_name')
        return render(request, 'user_profile/ajax_edit_clinical_setting.html',{'edit_id':edit_id,
                                                                               'pract_detail':pract_detail,
                                                                               'clinical_setting':clinical_setting,
                                                                               'index':index,
                                                                               'user_id':request.GET.get('user_id') if request.GET.get('user_id') else None
                                                                               })
        
def delete_clinical_data(request):
    user_json = {}
    if request.method == "GET":
        pract_details = PractDetails.objects.get(clinical_setting={'clinic_id':request.GET.get('clinical_id')}, user_id=request.GET.get('user_id'))
        pract_detail_pop = pract_details.clinical_setting.pop(int(request.GET.get('index_no'))-1)
        pract_details.save()
    if pract_detail_pop:                                  
        success = _('Clinical Setting Deleted Successfully')
    else:
        success = _('Failed, Clinical Setting Add.Please Try Again')
    user_json['success'] = success
    return JsonResponse(user_json)
"""Clinical Setting ADD, Update, Delete Functionality --Ends Here"""

"""Registration Step2 Function Ends here"""


"""Registration Success page redirect view function starts here"""
def registration_successfuly(request):
    if request.method == "GET":
        return render(request, 'user_profile/registration_success_page.html',{})

"""Activation Account based on the email verification starts here"""
def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            activation_message = _('Thank you for your email confirmation. Please wait for admin approval to start using this portal.') 
            return render(request, "user_profile/email_verification.html",{
                                           'activation_message':activation_message,
                                            'home_url':settings.CCRH_HOME_URL,
                                            })
                                                                                
        else:
            activation_message = _('You have already used this link for email verification. Please wait for admin approval to start using this portal.') 
            return render(request, "user_profile/email_verification.html",
                                            {'activation_message':activation_message,
                                            'home_url':settings.CCRH_HOME_URL,
                                            })

"""Activation Account based on the email verification ends here"""


"""Register uploaded certificate download function starts here"""
def uploaded_document_downloaded(request,doc_id=None):
    if request.method == "GET":
        if doc_id:
            if PractDetails.objects.filter(_id=doc_id).exists():
                file_name = PractDetails.objects.get(_id=doc_id).document_path
            elif CaseRepertorisation.objects.filter(case_id=doc_id).exists():
                file_name = CaseRepertorisation.objects.get(case_id=doc_id).computerized_manual_report
        else:
            file_name = None
        if file_name:
            file_path = settings.MEDIA_ROOT +'/'+ str(file_name)
            file_wrapper = FileWrapper(open(file_path,'rb'))
            file_mimetype = mimetypes.guess_type(file_path)
            response = HttpResponse(file_wrapper, content_type=file_mimetype )
            response['X-Sendfile'] = file_path
            response['Content-Length'] = os.stat(file_path).st_size
            response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(os.path.basename(file_name.file.name))
            return response
"""Register uploaded certificate download function ends here"""


"""For getting the description of notifications - Starts"""
def view_registration_details(request, notify_id=None):
    if request.method == "GET":
        try:
            record = Notification.objects.get(id=notify_id, recipient_id=request.user)
        except:
            record = None
        try:
            certificate_upload = PractDetails.objects.get(user_id = record.actor_object_id)
        except:
            certificate_upload = None
        try:
            aditional_profile = AdditionalProfile.objects.get(user_id = record.actor_object_id)
        except:
            aditional_profile = None
        if record:
            #Marking as Read once the user viewed
            mark_as_read(request, slug=record.slug)
        succes_page = request.session.pop('succes_page', None)
        return render(request, "user_profile/view_registration_details.html", {'record':record,
                                                                                'certificate_upload':certificate_upload,
                                                                                'aditional_profile':aditional_profile,
                                                                                'notify_id':notify_id,
                                                                                'succes_page':succes_page,
                                                                                })

    elif request.method == "POST":
        #Generating random password here
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(8)])
        #updating the profile information
        pract_obj = PractDetails.objects.filter(user_id = request.POST.get('practical_details_id')).update(pract_reg_no = request.POST.get('regsr_no'))
        
        '''inserting an certificate in practitioner details --starts here'''
        register_certificate = request.FILES.get('document_path')
        if register_certificate:
            pract_dtl = PractDetails.objects.get(user_id = request.POST.get('practical_details_id'))
            pract_dtl.document_path = register_certificate
            pract_dtl.save()
        '''inserting an certificate in practitioner details --ends here'''
                
        try:
            user_obj = AdditionalProfile.objects.get(user_id = request.POST.get('additona_profile_id'))
            user_obj.profile_status = request.POST.get('prfile_status_id')
            if user_obj.profile_status.lower() == "approved" or user_obj.profile_status.lower() == "revert" or user_obj.profile_status.lower() == "pending for approval":
                user_obj.profile_info = ProfileInfoAdditionalProfile(
                            profile_approved_by_id = request.user.id,
                            profile_approved_datetime = datetime.datetime.now(),
                            )
                user_obj.save()
        except:
            user_obj = None
        try:
            password_update = User.objects.get(id = user_obj.user_id)
            password_update.set_password(random_string)
            password_update.save()
        except:
            password_update = None
            
        """If admin can approved we are sending an email and paswword for login starts here"""
        if settings.SEND_MAIL_ALL_PLACE and user_obj.profile_status.lower() == "approved" :
            send_email = EmailTemplate.objects.get(email_code='CCEM001')
            subject = send_email.email_subject
            to_email = user_obj.user.email
            from_email, to = settings.ADMIN_EMAIL, [to_email]
            html_content = send_email.email_body.format(user_name=user_obj.user.first_name +' '+ user_obj.user.last_name,
                                                        email_id = user_obj.user.email,
                                                        password=random_string)
            text_content = format_html(html_content)
            email = EmailMultiAlternatives(subject,
                                            text_content,
                                            from_email,
                                            to)
            email.content_subtype = 'html'
            email.send()

        """If admin can select revert we are sending again registration link for update starts here"""
        if settings.SEND_MAIL_ALL_PLACE and user_obj.profile_status.lower() == "revert":
            send_email = EmailTemplate.objects.get(email_code='CCEM002')
            subject = send_email.email_subject
            to_email = user_obj.user.email
            from_email, to = settings.ADMIN_EMAIL, [to_email]
            current_site = Site.objects.get_current()
            html_content = send_email.email_body.format(user_name=user_obj.user.first_name +' '+ user_obj.user.last_name,
                                                        message = request.POST.get('message'),
                                                        user_id = user_obj.user.id,
                                                        domain= current_site.domain,
                                                        uid= urlsafe_base64_encode(force_bytes(user_obj.user.id)).encode().decode(),
                                                        token= account_activation_token.make_token(user_obj.user),
                                                        scheme= 'http',
                                                        fronted_reg = "fr",
                                                        activate_url='/en/user/registration'
                                                            )
            text_content = format_html(html_content)
            email = EmailMultiAlternatives(subject,
                                            text_content,
                                            from_email,
                                            to)
            email.content_subtype = 'html'
            email.send()
            #sending Email After saving ends
        request.session['succes_page'] = "Registration details updated successfully"
        return HttpResponseRedirect(reverse_lazy('user_profile:view_registration_details',args=[str(request.POST.get('notify_id'))]))
"""For getting the description of notifications - Ends"""

    
"""Based on clinical name fetch other details starts here"""
def get_hospital_details(request):
    if request.method == "GET":
        if  request.GET.get('clinic_id'):
            type_list = HospitalMaster.objects.filter(_id=request.GET.get('clinic_id')).values('address_1','address_2','pincode','city')
            clinic_obj_id = json.loads(json_util.dumps(type_list))
            return JsonResponse({'list':clinic_obj_id})
"""Based on clinical name fetch other details ends here"""

"""Calling Ajax Based on the state showing City starts here"""
def get_city_based_on_state(request):
    if request.method == "GET":
        results=[]
        try:
            state_obj = State.objects.get(_id = request.GET.get('state_name'))
        except:
            state_obj = None
        city_names = City.objects.filter(state_id = state_obj)
        for fos in city_names:
            user_json = {}
            user_json['id'] = json.loads(json_util.dumps(fos._id))['$oid']
            user_json['city_name'] = fos.city_name
            results.append(user_json)
        return JsonResponse({'list':results
                                 })
"""Calling Ajax Based on the state showing City Ends here"""


"""Based on the auto complete showing an Hospital Name details Starts here"""
def get_hospital_names(request):
    results=[]
    if request.method == "GET":
        if request.GET.get('value'):
            type_list = HospitalMaster.objects.filter(hospital_name__icontains = request.GET.get('value'),hospital_type_id=request.GET.get('checking_clinical_type_id'))
            for fos in type_list:
                 user_json = {}
                 user_json['id'] = json.loads(json_util.dumps(fos._id))
                 user_json['value'] = fos.hospital_name
                 results.append(user_json)
            return JsonResponse({'list':results})
        elif request.GET.get('hosiptal_nam'):
            type_list = HospitalMaster.objects.filter(hospital_name=request.GET.get('hosiptal_nam'))
            for fos in type_list:
                user_json = {}
                user_json['hospital_name'] = fos.hospital_name
                user_json['address_1'] = fos.address_1
                user_json['address_2'] = fos.address_2
                user_json['pincode'] = fos.pincode
                user_json['city'] = fos.city.city_name
                user_json['city_id'] = json.loads(json_util.dumps(fos.city_id))
                user_json['state'] = fos.state.state_name
                user_json['state_id'] = json.loads(json_util.dumps(fos.state_id))
                results.append(user_json)
            return JsonResponse({'list':results})
"""Based on the auto complete showing an Hospital Name details Ends here"""

"""Based on the auto complete showing an City Name details Starts here"""
def get_city_names(request):
    results=[]
    if request.method == "GET":
        if request.GET.get('value'):
            type_list = City.objects.filter(city_name__icontains = request.GET.get('value'))
            for fos in type_list:
                         user_json = {}
                         user_json['id'] = json.loads(json_util.dumps(fos._id))
                         user_json['value'] = fos.city_name
                         results.append(user_json)
            return JsonResponse({'list':results})
"""Based on the auto complete showing an City Name details Ends here"""

"""Based on the auto complete showing an City Name details Starts here"""
def get_state_names(request):
    results=[]
    if request.method == "GET":
        if request.GET.get('value'):
            type_list = State.objects.filter(state_name__icontains = request.GET.get('value'))
            for fos in type_list:
                         user_json = {}
                         user_json['id'] = json.loads(json_util.dumps(fos._id))
                         user_json['value'] = fos.state_name
                         results.append(user_json)
            return JsonResponse({'list':results})
"""Based on the auto complete showing an City Name details Ends here"""

"""To fetch the State name based on auto complete  --starts here"""
class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = State.objects.all()
        if self.q:
            qs = qs.filter(state_name__icontains=self.q)
        return qs

"""To fetch the State name based on auto complete --ends here"""

"""To fetch the City name based on auto complete  --starts here"""
class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(city_name__icontains=self.q)
        return qs

"""To fetch the City name based on auto complete --ends here"""

"""To fetch the Hospital name based on auto complete  --starts here"""
class HospitalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = HospitalMaster.objects.all()

        if self.q:
            qs = qs.filter(hospital_name__icontains=self.q)
        return qs
"""To fetch the Hospital name based on auto complete --ends here"""

"""Search functionality of New User Panel Mapping --Starts Here"""
def new_create_user_panel(request):
    if request.method == "GET":
        category = CaseCategory.objects.all()
        user = User.objects.all()
        success_msg = request.session.pop('success_msg', None)
        search_list = {}
        if request.GET.get('panel_name'):
            search_list['panel_name__icontains'] = request.GET.get('panel_name')
#         if request.GET.get('category'):
#             search_list['category'] = request.GET.get('category')
#         if request.GET.get('supervisorpool'):
#             search_list['supervisor_pool'] = request.GET.get('supervisorpool')
#         if request.GET.get('reviewerpool'):
#             search_list['reviewer_pool'] = request.GET.get('reviewerpool')
#         records = PanelUserGroupMapping.objects.filter(category={'category':request.GET.get('category')})

        records = PanelUserGroupMapping.objects.filter(**search_list).order_by('-panel_name')
        page = request.GET.get('page')
        paginator = Paginator(records, 10)
        records = paginator.get_page(page)
        return render(request, "user_profile/user_panel_mapping_list.html",{'category':category,
                                                                              'user':user,
                                                                              'records':records,
                                                                              'success_msg':success_msg,
                                                                              'panel_name':request.GET.get('panel_name'),
#                                                                               'category_search':request.GET.get('category'),
#                                                                               'supervisorpool_search':int(request.GET.get('supervisorpool')) if request.GET.get('supervisorpool') else None,
#                                                                               'reviewerpool_search':int(request.GET.get('reviewerpool')) if request.GET.get('reviewerpool') else None,
                                                                            })
"""Search functionality of New User Panel Mapping --Ends Here"""

"""Create/Edit/Delete functionality of New User Panel Mapping --Starts Here"""
# Category, SupervisorPool, ReviewerPool

def create_user_panel(request, edit_id=None):
    if request.method == "GET":
        edit_record = None
        category = CaseCategory.objects.all()
        user = User.objects.all()
        reviewer_user = User.objects.filter(groups__name='Reviewer')
        supervisor_user = User.objects.filter(groups__name='Supervisor')
        

        success_msg = request.session.pop('success_msg', None)
        try:
            edit_record = PanelUserGroupMapping.objects.get(_id=edit_id)
        except:
            edit_record = None
        return render(request, "user_profile/create_user_panel_mapping.html",{'category':category,
                                                                              'user':user,
                                                                              'reviewer_user':reviewer_user,
                                                                              'supervisor_user':supervisor_user,
                                                                              'edit_record':edit_record,
                                                                              'success_msg':success_msg,})
    elif request.method == "POST":
        cat_list = []
        sup_list = []
        rev_list = []
        postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^category_\d+', key)]
        if postdata_keys:
            for each in postdata_keys:
                if  request.POST.get("category_%s" % each, None):
                    category_value = request.POST.get("category_%s" % each, None)
                    category_list = [Category(category = CaseCategory.objects.get(_id = category_value))]
                cat_list.extend(category_list)
        postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^supervisorpool_\d+', key)]
        if postdata_keys:
            for each in postdata_keys:
                if  request.POST.get("supervisorpool_%s" % each, None):
                    supervisor_value = request.POST.get("supervisorpool_%s" % each, None)
                    supervisor_list = [SupervisorPool(supervisor = User.objects.get(id = supervisor_value))]
                sup_list.extend(supervisor_list)
        postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^reviewerpool_\d+', key)]
        if postdata_keys:
            for each in postdata_keys:
                if  request.POST.get("reviewerpool_%s" % each, None):
                    reviewer_value = request.POST.get("reviewerpool_%s" % each, None)
                    reviewer_list = [ReviewerPool(reviewer = User.objects.get(id = reviewer_value))]
                rev_list.extend(reviewer_list)
        
        delete_id = request.POST.get('delete_id', None)
        if delete_id:
            #Delete condition for user panel
            PanelUserGroupMapping.objects.filter(_id=delete_id).delete()
            request.session['success_msg'] = _('User Panel has been deleted successfully.')

        elif cat_list and sup_list and rev_list and not edit_id:
            #Create condition for user panel
            PanelUserGroupMapping.objects.create(panel_name=request.POST.get("panel_name"),
                                    category = cat_list,
                                    supervisor_pool = sup_list,
                                    reviewer_pool=rev_list)
            request.session['success_msg'] = _("User Panel has been created successfully.")

        elif cat_list and sup_list and rev_list and edit_id:
            #Update condition for user panel
            PanelUserGroupMapping.objects.filter(_id = edit_id).update(panel_name=request.POST.get("panel_name"),
                                    category = cat_list,
                                    supervisor_pool = sup_list,
                                    reviewer_pool=rev_list)
            request.session['success_msg'] = _("User Panel has been updated successfully.")
        elif request.POST.get('delete_index_no'):
            panel_data = PanelUserGroupMapping.objects.get(_id = edit_id)
            if request.POST.get('delete_type') == 'Category':
                panel_data.category.pop(int(request.POST.get('delete_index_no'))-1)
                panel_data.save()
                request.session['success_msg'] = _("Category has been removed successfully.")
            elif request.POST.get('delete_type') == 'Supervisor':
                panel_data.supervisor_pool.pop(int(request.POST.get('delete_index_no'))-1)
                panel_data.save()
                request.session['success_msg'] = _("Supervisor has been removed successfully.")
            elif request.POST.get('delete_type') == 'Reviewer':
                panel_data.reviewer_pool.pop(int(request.POST.get('delete_index_no'))-1)
                panel_data.save()
                request.session['success_msg'] = _("Reviewer has been removed successfully.")
            return HttpResponseRedirect(reverse_lazy('user_profile:create_user_panel', args=[edit_id]))
    return HttpResponseRedirect(reverse_lazy('user_profile:new_create_user_panel'))
"""Create/Edit/Delete functionality of New User Panel Mapping --Ends Here"""
