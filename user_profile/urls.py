from django.urls import path, re_path,include
from django.conf.urls import url
from user_profile import views as user_profile_views
from django.contrib.auth.views import PasswordResetConfirmView,PasswordResetCompleteView, PasswordResetView
from user_profile.forms import CustomSetPasswordForm, PasswordResetFormUnique, CustomPasswordChangeForm
from user_profile.views import StateAutocomplete, CityAutocomplete,HospitalAutocomplete


app_name="user_profile"

urlpatterns = [
    path('check_user/', user_profile_views.check_user_api, name="check_user"),
#     path('check_user_forgot_api/',user_profile_views.check_user_forgot_api, name="check_user_forgot_api"),
    path('login/', user_profile_views.login_view, name="login"),
    path('logout/', user_profile_views.logout_view, name='logout'),
    path('change_password/', user_profile_views.change_password, name='change_password'),
#     path('forget_password/', user_profile_views.password_forgot, name='forget_password'),
#     path('password-forgot/', user_profile_views.password_forgot, name='password_forgot'),
#     #On click of password reset link, displaying a form to submit passwords.
#     path('password_reset_<uidb64>_<token>/',PasswordResetConfirmView.as_view(
#                                             form_class=CustomSetPasswordForm,
#                                             template_name='user_profile/password_reset_confirm.html',
#                                             success_url='/user/reset/done/'),
#                                             name='password_reset_confirm'),
#     #After password resetting done redirecting to a page having login link.
#     path('reset/done/', PasswordResetCompleteView.as_view(
#                                                 template_name='user_profile/password_reset_complete.html'
#                                                 ), name='password_reset_complete'),
#     path('registration/<str:uidb64>/<str:backend_reg>', user_profile_views.registration_profile_info, name='profile_info'),
#     path('documentation_upload/', user_profile_views.registration_document_upload, name='documentation_upload'),
    path('register_success/', user_profile_views.registration_successfuly, name='register_success'),
    path('get_city_name/',  user_profile_views.get_city_based_on_state, name='get_city_name'),
    path('uploaded_document_downloaded/<str:doc_id>/',  user_profile_views.uploaded_document_downloaded, name='uploaded_document_downloaded'),
    path('view_registration_details/<str:notify_id>/', user_profile_views.view_registration_details, name='view_registration_details'),
    path('activate/<uidb64>/<token>/',user_profile_views.activate, name='activate'),
    path('get_hospital_names/',  user_profile_views.get_hospital_names, name='get_hospital_names'),
    
    path('reset-password/verify-token/', user_profile_views.CustomPasswordTokenVerificationView.as_view(), name='password_reset_verify_token'),
    path('reset-password/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('clinical_settings_data/',  user_profile_views.clinical_settings_data, name='clinical_settings_data'),
    url(r'^state-autocomplete/$',StateAutocomplete.as_view(),name='state-autocomplete',),
    url(r'^city-autocomplete/$',CityAutocomplete.as_view(),name='city-autocomplete',),
    url(r'^Hospital-autocomplete/$',HospitalAutocomplete.as_view(),name='Hospital-autocomplete',),
    path('clinical_setting_data_edit/<str:edit_id>/<int:index>/', user_profile_views.clinical_setting_data_edit, name='clinical_setting_data_edit'),
    path('delete_clinical_data/', user_profile_views.delete_clinical_data, name='delete_clinical_data'),
    path('get_hospital_details/', user_profile_views.get_hospital_details, name='get_hospital_details'),
    path('get_city_names/',  user_profile_views.get_city_names, name='get_city_names'),
    path('get_state_names/',  user_profile_views.get_state_names, name='get_state_names'),
    re_path(r'^registration/(?:(?P<uidb64>\w+)/(?P<br>\w+))?$', user_profile_views.registration_profile_info, name="profile_info"), 
    re_path(r'^documentation_upload/(?:(?P<user_id>\w+)/(?P<br>\w+))?$', user_profile_views.registration_document_upload, name="documentation_upload"), 

    path('new_create_user_panel', user_profile_views.new_create_user_panel, name="new_create_user_panel"),
    re_path(r'^create_user_panel/(?:(?P<edit_id>\w+)/)?$', user_profile_views.create_user_panel, name='create_user_panel'),


    ]