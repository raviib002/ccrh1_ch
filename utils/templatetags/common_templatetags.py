from django import template
import urllib.parse
register = template.Library()
from urllib.parse import urlencode
from django.contrib.auth.models import User, Group
import os
from django.conf import settings
from case_history.models import (CaseComplaints, CaseHistory, CaseHistoryPatientDetail,
                                 CasePersonalHistory, CaseMentalGeneral, CaseFamilyHistory,
                                 CaseGynaecologicalHistory, CaseRepertorisation, CaseMiasamaticAnalysis,
                                 CasePersonalHistory,CasePhysicalExaminationFindings,CasePastHistory,
                                 CaseObstetricHistory)

from master.models import City, State
from user_profile.models import PractDetails


@register.filter(is_safe=True)
def convert_to_int(value):
    try:
        if value:
            return int(value)
    except:
        return None
"""Convert other datatypes to Integer - ends"""

"""To get the file name - starts """
@register.filter(is_safe=True)
def get_filename(value):
    try:
        return os.path.basename(value.file.name)
    except:
        return ''
    
# Get settings value in template
@register.simple_tag
def settings_value(name):
    return getattr(settings, name, "")

"""Based on the case id fetching latest record of medicine starts here"""
# Get settings value in template
# @register.filter(is_safe=True)
# def medicine_latest_value(case_id_value):
#     try:    
#         medicine_management = CaseMedicineManagement.objects.get(case_id = case_id_value, prescription_order=1).id
#     except:
#         medicine_management = None
#     medicine_mapping = MedicinePrescriptionMapping.objects.filter(medi_mgnt_id=medicine_management).values_list('prescription__med_name',flat=1).last()
#     return medicine_mapping if medicine_mapping else 'NA'
# 
# """Based on the case id fetching latest record of disease starts here"""
# # Get settings value in template
# @register.filter(is_safe=True)
# def disease_latest_record(case_id):
#     dises_mmstr = CaseDiagnosis.objects.filter(case_id=case_id,is_primary=1).values_list('dis__dis_name',flat=1).last()
#     return dises_mmstr
#     
# """Based on the case id fetching latest record of symptoms starts here"""
# # Get settings value in template
# @register.filter(is_safe=True)
# def symptoms_latest_record(case_id):
#     symptom_mast = CaseComplaints.objects.filter(case_id=case_id).values_list('comp_symptoms__sym_name',flat=1).last()
#     return symptom_mast
     

"""Based on the table header we are changing the order_by starts here - Manish """
@register.filter(is_safe=True)
def url_replace(request, field, value, direction=''):
    dict_ = request.GET.copy()

    if field == 'order_by' and field in dict_.keys():          
      if dict_[field].startswith('-') and dict_[field].lstrip('-') == value:
        dict_[field] = value
      elif dict_[field].lstrip('-') == value:
        dict_[field] = "-" + value
      else:
        dict_[field] = direction + value
    else:
      dict_[field] = direction + value

    return urlencode(OrderedDict(sorted(dict_.items())))
"""Based on the table header we are changing the order_by Ends here - Manish """
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return urllib.parse.urlencode(d)

"""Convert string to List starts here"""
@register.filter(is_safe=True)
def string_to_list(value):
    return eval(value)

"""Convert get city name from city id """
@register.filter(is_safe=True)
def get_city_name(city_id):
    city = City.objects.get(_id=city_id)
    return city.city_name

"""Convert get state name from state id """
@register.filter(is_safe=True)
def get_state_name(state_id):
    city = State.objects.get(_id=state_id)
    return city.state_name

"""To get role of user """
@register.filter(is_safe=True)
def get_role_name(user_id):
    if user_id:
        user = User.objects.get(id=user_id)
        return user.groups.all()[0]
    
"""To get the doctor name based on registration no """
@register.filter(is_safe=True)
def get_doctor_name(regis_no):
    if regis_no:
        try:
            pract = PractDetails.objects.filter(pract_reg_no=regis_no).last()
            return pract.user.first_name+' '+pract.user.last_name
        except:
            return 'NA'

"""To get the patient name based on registration no """
@register.filter(is_safe=True)
def get_patient_name(case_id):
    if case_id:
        try:
            patient_details = CaseHistoryPatientDetail.objects.filter(case__case_id=case_id).last()
            return patient_details.case_patient_name
        except:
            return 'NA'
       
"""To check the table data saved"""
@register.filter(is_safe=True)
def check_table_data_saved(case_id, tab_name):
    if CaseHistory.objects.filter(_id=case_id).exists() and tab_name=='add_case':
        return True
    elif CaseHistoryPatientDetail.objects.filter(case___id=case_id).exists() and tab_name=='patient_details':
        return True
    elif CaseComplaints.objects.filter(case___id=case_id).exists() and tab_name=='present_complaint':
        return True
    elif CasePersonalHistory.objects.filter(case___id=case_id).exists() and tab_name=='personal_history':
        return True
    elif CaseMentalGeneral.objects.filter(case___id=case_id).exists()and tab_name=='mental_general':
        return True
    elif CasePastHistory.objects.filter(case___id=case_id).exists()and tab_name=='past_general':
        return True
    elif CaseFamilyHistory.objects.filter(case___id=case_id).exists()and tab_name=='family_history':
        return True
    elif CaseGynaecologicalHistory.objects.filter(case___id=case_id).exists()and tab_name=='gynaecological_history':
        return True
    elif CaseObstetricHistory.objects.filter(case___id=case_id).exists()and tab_name=='obstreric_history':
        return True
    elif CaseRepertorisation.objects.filter(case___id=case_id).exists()and tab_name=='repertorisation':
        return True
    elif CasePhysicalExaminationFindings.objects.filter(case___id=case_id).exists()and tab_name=='physical_examination_finding':
        return True
    elif CaseMiasamaticAnalysis.objects.filter(case___id=case_id).exists()and tab_name=='miasamatic_analysis':
        return True


    
"""To get the _id from queryset"""
@register.filter(is_safe=True)
def get_id(obj, attribute):
    return getattr(obj, attribute)

"""To get word from list of string"""
@register.filter(is_safe=True)
def get_string_value(str):
    new_str = ""  
    s = eval(str)
    for i in s:
        if new_str == "":
            new_str += i   
        else:
            new_str += ', '+i   
    return new_str

@register.filter(name='split')
def split(value, key):
    """Returns the value turned into a list."""
    return value.split(key)

register.filter('param_replace', param_replace)