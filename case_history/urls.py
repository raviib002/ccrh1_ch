from django.urls import path, re_path
from django.conf.urls import url
from case_history import views as case_history_views
from case_history.views import ( SymptomsAutocomplete, DiseaseAutocomplete, MentalAutocomplete, 
                                 StateAutocomplete ,CityAutocomplete , InstituteAutocomplete,
                                 MedicineAutocomplete 
                                 )
app_name="case_history"

urlpatterns = [
        path('dashboard/', case_history_views.dashboard, name='dashboard'),
        path('get_symptoms_names/', case_history_views.get_symptoms_names, name='get_symptoms_names'),
        path('get_investigation_category/', case_history_views.get_investigation_category, name='get_investigation_category'),
        re_path(r'^add_case/(?:(?P<case_id>\w+)/)?$', case_history_views.add_case, name="add_case"), 
        re_path(r'^patient_details/(?:(?P<case_id>\w+)/)?$', case_history_views.patient_details, name="patient_details"), 
        re_path(r'^present_complaint/(?:(?P<case_id>\w+)/)?$', case_history_views.present_complaint, name="present_complaint"), 
        re_path(r'^personal_history/(?:(?P<case_id>\w+)/)?$', case_history_views.personal_history, name="personal_history"), 
#         re_path(r'^physical_general/(?:(?P<case_id>\d+)/)?$', case_history_views.physical_general, name="physical_general"), 
        re_path(r'^mental_general/(?:(?P<case_id>\w+)/)?$', case_history_views.mental_general, name="mental_general"), 
        re_path(r'^past_general/(?:(?P<case_id>\w+)/)?$', case_history_views.past_general, name="past_general"), 
        re_path(r'^family_history/(?:(?P<case_id>\w+)/)?$', case_history_views.family_history, name="family_history"), 
        re_path(r'^gynaecological_history/(?:(?P<case_id>\w+)/)?$', case_history_views.gynaecological_history, name="gynaecological_history"), 
        re_path(r'^obstreric_history/(?:(?P<case_id>\w+)/)?$', case_history_views.obstreric_history, name="obstreric_history"), 
        re_path(r'^repertorisation/(?:(?P<case_id>\w+)/)?$', case_history_views.repertorisation, name="repertorisation"), 
        re_path(r'^miasamatic_analysis/(?:(?P<case_id>\w+)/)?$', case_history_views.miasamatic_analysis, name="miasamatic_analysis"), 
        re_path(r'^physical_examination_finding/(?:(?P<case_id>\w+)/)?$', case_history_views.physical_examination_finding, name="physical_examination_finding"), 
#         re_path(r'^investigations_categories/(?:(?P<case_id>\d+)/)?$', case_history_views.investigations_categories, name="investigations_categories"), 
#         re_path(r'^medical_management/(?:(?P<case_id>\d+)/)?$', case_history_views.medical_management, name="medical_management"), 
#         re_path(r'^add_on_therapies/(?:(?P<case_id>\d+)/)?$', case_history_views.add_on_therapies, name="add_on_therapies"), 
        path('get_disease_names/', case_history_views.get_disease_names, name='get_disease_names'),
        url(r'^symptoms-autocomplete/$',SymptomsAutocomplete.as_view(),name='symptoms-autocomplete',),
        url(r'^disease-autocomplete/$',DiseaseAutocomplete.as_view(),name='disease-autocomplete',),
        url(r'^mental-autocomplete/$',MentalAutocomplete.as_view(),name='mental-autocomplete',),
#         path('get_medicine_names/', case_history_views.get_medicine_names, name='get_medicine_names'),
#         re_path(r'^follow_up_add/(?:(?P<order_no>\d+)/)?$', case_history_views.follow_up_add, name="follow_up_add"), 
#         path('case_submitted_status/', case_history_views.case_submitted_status, name='case_submitted_status'),
#         re_path(r'^case_submitted_status/(?:(?P<case_id>\d+)/)?$', case_history_views.case_submitted_status, name="case_submitted_status"), 
        url(r'^institute-autocomplete/$',InstituteAutocomplete.as_view(),name='institute-autocomplete',),
        url(r'^state-autocomplete/$',StateAutocomplete.as_view(),name='state-autocomplete',),
        url(r'^city-autocomplete/$',CityAutocomplete.as_view(),name='city-autocomplete',),
        
        url(r'^institute-autocomplete/$',InstituteAutocomplete.as_view(),name='institute-autocomplete',),
        path('get_keywords_names/', case_history_views.get_keywords_names, name='get_keywords_names'),
        url(r'^medicine-autocomplete/$',MedicineAutocomplete.as_view(),name='medicine-autocomplete',),
        
#         re_path(r'^follow_up_practitioners/(?:(?P<case_id>\w+)/)?$', case_history_views.follow_up_practitioners, name="follow_up_practitioners"), 

    ]