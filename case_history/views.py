import re
from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from django.urls.base import reverse_lazy
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Q,F, Value as V
from django.db.models.functions import Concat
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator
from django.conf import settings
from functools import reduce
import operator
from master.models import (State, City, SymptomsMaster, DiseaseMaster, HospitalMaster,
                           HabitsMaster, DietsMaster, MentalGeneralMaster, MedicineMaster
                           )
from case_history.models import (CaseHistory, CaseComplaints, Symptoms ,SymptomsForm,
                                    Keywords, KeywordsDisease, KeywordsSymptoms, OtherDiagnosis,
                                    Diagnosis, CaseHistoryPatientDetail, Habits, Diets,
                                    EvolutionaryHistory,HabitsForm, DietsForm,
                                    EvolutionaryHistoryForm ,MentalGeneralsForm,
                                    MentalGenerals, CaseMentalGeneral, CasePersonalHistory,
                                    CaseFamilyHistory,FamilyHistory,Diseases,PresentDiseases,
                                    CaseGynaecologicalHistory,
                                    Menarche,MenarcheForm,
                                    MenstrualCycleParticulars,
                                    Lmp, LmpForm, Bleeding, BleedingForm, Cycle, CycleForm, Colour, ColourForm, 
                                    Consistency, ConsistencyForm, Odour, OdourForm, Character, CharacterForm,
                                    Dysmenorrhoea, DysmenorrhoeaForm, Complaints, ComplaintsForm,
                                    AbnormalDischarge,
                                    Leucorrhea, LeucorrheaForm, BleedingPerVagina, BleedingPerVaginaForm,
                                    Menopause, MenopauseForm,
                                    HoGynaecologicalSurgeries,
                                    Hysterectomy, HysterectomyForm, Others, OthersForm,
                                    ContraceptiveMethods, ContraceptiveMethodsForm,
                                    CaseRepertorisation,
                                    SymptomsRepertorized, SymptomsRepertorizedForm,
                                    Medicine, MedicineForm,
                                    CaseMiasamaticAnalysis, PredominantMiasm,
                                    CasePastHistory,PastHistory,HistoryOfSuppression,
                                    PastHistoryForm,HistoryOfSuppressionForm,HistoryOfChildren,BirthHistory,DeliveryHisDetails,MotherHealthHistory,
                                    BreastFeedingHistory,BirthHistoryForm,DeliveryHisDetailsForm,MotherHealthHistoryForm,BreastFeedingHistoryForm,
                                    GeneralExaminationForm,GeneralExamination,SystemicExamination,SystemicExaminationForm,CasePhysicalExaminationFindings,
                                    CaseObstetricHistory,ObstetricHistory, ObstetricHistoryForm,
                                    Pregnancy,
                                    Antenatal, AntenatalForm,
                                    ComplaintsDuringPregnancy, ComplaintsDuringPregnancyForm,
                                    NatureOfLabor,NatureOfLaborForm,
                                    Postnatal,PostnatalForm,
                                    Child, ChildForm
                                )

from case_history.forms import (AddCaseDetailsForm, PatientDetailsForm, PersonalHistoryForm,
                               )
from django.forms import modelformset_factory,formset_factory,inlineformset_factory
from django.template.context_processors import request
import requests
from dal import autocomplete
from utils.common_functions import (data_as_list, data_as_past_supression_list) 
from user_profile.models import PractDetails
from bson import json_util, ObjectId


""" Dashboard functionality  - Starts"""
@login_required
def dashboard(request):
    if request.method == "GET":
        practi_id = PractDetails.objects.filter(user_id = request.user.id).values_list('pract_reg_no', flat=True).last()
        city_list = None
        search_filter_list = {}
        my_search_filter = {}
        if request.GET.get('case_id'):
            search_filter_list['case_id'] = request.GET.get('case_id')
        if request.GET.get('patient_name'):
            search_filter_list['casehistorypatientdetail__case_patient_name__icontains'] = request.GET.get('patient_name')
#        if request.GET.get('strt_date'):
#            search_filter_list['created_date__gte'] = request.GET.get('strt_date')
#        if request.GET.get('end_date'):
#            search_filter_list['created_date__lte'] = request.GET.get('end_date')
        if request.GET.get('gender'):
            search_filter_list['casehistorypatientdetail__case_patient_sex'] = request.GET.get('gender')
        if request.GET.get('dis_name'):
            search_filter_list['diagnosis'] = {'primary_diagnosis_id': int(request.GET.get('dis_name'))} 
        if request.GET.get('medi_name'):
            search_filter_list['casehistory__prescription'] = request.GET.get('medi_name')
        if request.GET.get('sympt_name'):
            search_filter_list['keyword_index__icontains'] = request.GET.get('sympt_name')
        if request.GET.get('location_name'):
            search_filter_list['casehistorypatientdetail__case_patient_address__icontains'] = request.GET.get('location_name')
        if request.GET.get('city_name'):
            search_filter_list['casehistorypatientdetail__case_patient_city_id'] = request.GET.get('city_name')
        if request.GET.get('state_name'):
            search_filter_list['casehistorypatientdetail__case_patient_state_id'] = request.GET.get('state_name')
        if request.GET.get('status_name'):
            search_filter_list['case_status'] = request.GET.get('status_name')
        if request.GET.get('basic_search_value'):
            my_search_filter['case_pract_id'] = practi_id
            if request.GET.get('basic_search_value').isupper() and request.GET.get('basic_search_value').isalnum():
                my_search_filter['case_id'] = request.GET.get('basic_search_value')
            else:
                my_search_filter['case_title__icontains'] = request.GET.get('basic_search_value')
                
        case_histry_detals = CaseHistory.objects.filter(Q(**search_filter_list),Q(**my_search_filter),(Q(case_status="Accepted")|Q(case_pract_id = practi_id)|Q(case_reviewer_id = request.user.id)))
        
        #by doing group by fetching count of listing status starts here
        case_history_records = CaseHistory.objects.filter((Q(case_status="Accepted")|Q(case_pract_id = practi_id)|Q(case_reviewer_id = request.user.id)))
        case_listing_count = case_history_records.annotate(dcount=Count('case_status')).values_list('case_status')
        state_list=State.objects.all().values_list('_id','state_name')
        if request.GET.get('state_name'):
            city_list = City.objects.filter(state_id=request.GET.get('state_name')).values_list('_id','city_name')
           
        #dynamic paginations starts here
        page = request.GET.get('page')
        paginator = Paginator(case_histry_detals, settings.PAGINATION_COUNT)
        case_hstry_lst = paginator.get_page(page)
        pact_dtls = PractDetails.objects.filter()
        return render(request, 'case_history/dashboard.html',{
                                                            'data_list':case_hstry_lst,
                                                            'search_filter_list':search_filter_list,
                                                            'search_value' : request.GET.get('basic_search_value'),
                                                            'city':city_list,
                                                            'state':state_list,
                                                            'state_id':request.GET.get('state_name') if request.GET.get('state_name') else None,
                                                            'city_id':request.GET.get('city_name') if request.GET.get('city_name') else None,
                                                            'disease_nam':request.GET.get('disease_name'),
                                                            'comp_symptoms': request.GET.get('sympt_name'),
                                                            'prescription_name': request.GET.get('medicine_name'),
                                                            'gender' :request.GET.get('gender'),
                                                            'pat_name' : request.GET.get('patient_name'),
                                                            'location' : request.GET.get('location_name'),
                                                            'start_date' : request.GET.get('strt_date'),
                                                            'endd_date' : request.GET.get('end_date'),
                                                            'total_cases':len(case_listing_count),
                                                            'accpted_case':len(case_listing_count.filter(case_status="Accepted")),
                                                            'not_acceptes':len(case_listing_count.filter(case_status="Not Accepted")),
                                                            'under_review':len(case_listing_count.filter(case_status="Under Review")),
                                                            'statuss_name':request.GET.get('status_name'),
                                                            'pact_dtls':pact_dtls
                                                            })
""" Dashboard functionality  - Ends"""

"""CCRH add case history functionality - starts here"""
"""Case details functionality - starts here"""
@login_required
def add_case(request, case_id = None):
    if request.method == "GET":
#         auto_id = autogenerate_case_id
#         case_id = 'HCCR00012'
        success = request.session.pop('success_msg', None)
        try:
            case_record = CaseHistory.objects.get(_id = case_id)
        except:
            case_record = None
        #populating the record details and passing that data to form.
        if case_record:
            form = AddCaseDetailsForm(instance=case_record, user=request.user.id)
        else:
            form = AddCaseDetailsForm(user=request.user.id)
        return render(request, 'case_history/addcase.html',{'form':form,
                                                                'case_id':case_id,
                                                                'case_record':case_record,
#                                                                 'name_of_institute_unit':request.GET.get('institute_name'),
                                                                'success_note':success,
                                                            })
    elif request.method == "POST":
        form = AddCaseDetailsForm(request.POST, user=request.user.id)
        if form.is_valid():
            data = {k: v for k, v in form.cleaned_data.items()}
            other_diagnosis_list = []
            symptoms_keywords_list = []
            disease_keywords_list = []
            other_keyword_list = []
            keyword_index_list = []
            keywords_id = list(map(str,request.POST.getlist('keywords[]')))
            diagnosis_id = list(map(str,request.POST.getlist('diagnosis[]')))
            
            for i in diagnosis_id:
                other_list = [OtherDiagnosis(diagnosis=DiseaseMaster.objects.get(id=i))]
                other_diagnosis_list.extend(other_list)
                
            for i in keywords_id:
                if not i.isalpha() and not i.isnumeric()  and SymptomsMaster.objects.filter(_id=i).exists():
                    symptoms_list = [KeywordsSymptoms(keywords_symptoms=SymptomsMaster.objects.get(_id=i))]
                    symptoms_keywords_list.extend(symptoms_list)
                    sym_mastr = SymptomsMaster.objects.get(_id=i)
                    keyword_index_list.append(sym_mastr.sym_name)
                elif not i.isalpha() and DiseaseMaster.objects.filter(id=i).exists():
                    disease_list = [KeywordsDisease(keywords_disease=DiseaseMaster.objects.get(id=i))]
                    disease_keywords_list.extend(disease_list)
                    dis_mastr = DiseaseMaster.objects.get(id=i)
                    keyword_index_list.append(dis_mastr.dis_name)
                else:
                    other_keyword_list.append(i)
                    keyword_index_list.append(i)
            if request.POST.get('case_update'):
                case_list = CaseHistory.objects.filter(_id=request.POST.get('case_update')).update(
                                keyword_index = (','.join(keyword_index_list)),
                                **data)
                if case_list:
                    case_his = CaseHistory.objects.get(_id=request.POST.get('case_update'))
                    case_his.diagnosis = Diagnosis(primary_diagnosis = DiseaseMaster.objects.get(id=request.POST.get('primary_diagnosis')),
                                                other_diagnosis = other_diagnosis_list)
                    case_his.keywords = Keywords(case_keywords_symptoms = symptoms_keywords_list,
                                                case_keywords_disease = disease_keywords_list,
                                                other_keywords = (','.join(other_keyword_list)))
                    case_his.save()
                    case_id = case_his._id
                request.session['success_msg'] = _("Case Summary Details has been updated successfully.")
            else:
                case_list = CaseHistory.objects.create(
                                keywords = Keywords(
                                    case_keywords_symptoms = symptoms_keywords_list,
                                    case_keywords_disease = disease_keywords_list,
                                    other_keywords = (','.join(other_keyword_list))),
                                keyword_index = (','.join(keyword_index_list)),
                                diagnosis = Diagnosis(
                                    primary_diagnosis = DiseaseMaster.objects.get(id=request.POST.get('primary_diagnosis')),
                                    other_diagnosis = other_diagnosis_list),
                                case_status = request.POST.get('case_status'),
                                case_category = request.POST.get('case_category'),
                                **data)
                case_id = case_list._id
                request.session['success_msg'] = _("Case Summary Details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:patient_details', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please check the all mandatory fields carefully.")
            return HttpResponseRedirect(reverse_lazy('case_history:add_case', args=[case_id]))
"""Case details functionality - ends here"""

"""Patient details functionality - starts here"""
@login_required
def patient_details(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        #Getting the dynamic record based on the requested Case ID.
        try:
            case_record = CaseHistoryPatientDetail.objects.get(case_id=case_id)
        except:
            case_record = None
        #populating the record details and passing that data to form.
        if case_record:
            form = PatientDetailsForm(instance=case_record)
        else:
            form = PatientDetailsForm()
        return render(request,'case_history/patient_details.html',{'form':form,
                                                                    'case_id':case_id,
                                                                    'case_record':case_record,
                                                                    'success_note':success,
                                                                    })
    elif request.method == 'POST':
        form = PatientDetailsForm(request.POST)
        if form.is_valid() and case_id:
            data = {k: v for k, v in form.cleaned_data.items()}
            if request.POST.get("patient_dtls"):
                CaseHistoryPatientDetail.objects.filter(case_id=case_id).update(**data)
                request.session['success_msg'] = _("Patient Information Details has been updated successfully.")
            else:
                CaseHistoryPatientDetail.objects.create(case_id=case_id,
                                                                **data)
                request.session['success_msg'] = _("Patient Information Details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:present_complaint', args=[case_id]))
        elif not case_id:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:patient_details'))
        else:
            request.session['success_msg'] = _("Please check the all mandatory fields carefully.")
            return HttpResponseRedirect(reverse_lazy('case_history:patient_details', args=[case_id]))
            
"""Patient details functionality - ends here"""

"""Present complaints functionality - starts here"""
@login_required
def present_complaint(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        try:
            case_record = CaseComplaints.objects.get(case_id=case_id)
        except:
            case_record = None
        if  request.GET.get('symptoms_index'):
            form = SymptomsForm(instance = case_record.symptoms[int(request.GET.get('symptoms_index'))-1])
        else:
            form = SymptomsForm()
        return render(request,'case_history/present_complaints.html',{'form':form ,
                                                                      'case_id':case_id,
                                                                      'case_record':case_record,
                                                                      'success_note':success,
                                                                      'symptoms_index':request.GET.get('symptoms_index'),
                                                                      })
    elif request.method == 'POST':
        form = SymptomsForm(request.POST)
        try:
            complaint_obj = CaseComplaints.objects.get(case_id = case_id)
        except:
            complaint_obj = None
        if form.is_valid() and case_id:
            data = {k: v for k, v in form.cleaned_data.items()}
            if request.POST.get("symptoms_index"):
                complaint_obj.symptoms.pop(int(request.POST.get('symptoms_index'))-1)
                complaint_obj.symptoms.insert(int(request.POST.get('symptoms_index'))-1,Symptoms(**data))
                complaint_obj.save()
                request.session['success_msg'] = _("Presenting Complaints details has been updated successfully.")
            elif complaint_obj:
                complaint_obj.symptoms.extend([Symptoms(**data)])
                complaint_obj.save()
                request.session['success_msg'] = _("Presenting Complaints details has been saved successfully.")
            else:
                CaseComplaints.objects.create(case_id = case_id ,symptoms =[Symptoms(**data)])
                request.session['success_msg'] = _("Presenting Complaints details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:present_complaint', args=[case_id]))
        elif request.POST.get("delete_present_complaint"):
            complaint_obj.symptoms.pop(int(request.POST.get('index_no'))-1)
            complaint_obj.save()
            request.session['success_msg'] = _("Presenting Complaints details has been deleted successfully.")
        else:
            request.session['success_msg'] = _("Please check the all mandatory fields carefully.")
        if case_id:
            return HttpResponseRedirect(reverse_lazy('case_history:present_complaint', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:present_complaint'))
            
"""Present complaints functionality - ends here"""

"""Personal history functionality - starts here"""
@login_required
def personal_history(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        habit_master = HabitsMaster.objects.all()
        diet_master = DietsMaster.objects.all()
        try:
            personal_history = CasePersonalHistory.objects.filter(case___id=case_id).last()
            pers_his_form = PersonalHistoryForm(instance=personal_history)
        except:
            personal_history = None
            pers_his_form = PersonalHistoryForm()
        if (request.GET.get('habit_index_no') or request.GET.get('diet_index_no')) and personal_history:
            try:
                habit_form = HabitsForm(instance=personal_history.habits[int(request.GET.get('habit_index_no'))-1])
            except:
                habit_form = HabitsForm()
            try:
                diet_form = DietsForm(instance=personal_history.diets[int(request.GET.get('diet_index_no'))-1])
            except:
                diet_form = DietsForm()
        else:
            habit_form = HabitsForm()
            diet_form = DietsForm()
            
        return render(request,'case_history/personal_history.html',{'case_id':case_id,
                                                                    'habit_form':habit_form,
                                                                    'diet_form':diet_form,
                                                                    'pers_his_form':pers_his_form,
                                                                    'personal_history':personal_history,
                                                                    'habit_index_no':request.GET.get('habit_index_no'),
                                                                    'diet_index_no':request.GET.get('diet_index_no'),
                                                                    'success_note':success,
                                                                    'habit_master':habit_master,
                                                                    'diet_master':diet_master,
                                                                    })

    elif request.method == 'POST':
        try:
            pesonal_his = CasePersonalHistory.objects.get(_id=request.POST.get('personal_history'),case_id=case_id)
        except:
            pesonal_his = None
        try:
            pesonal_his = CasePersonalHistory.objects.get(case_id=case_id)
        except:
            pesonal_his = None
        if ("add_habit_data" in request.POST or 'edit_habit_data' in request.POST) and case_id:
            habit_form = HabitsForm(request.POST)
            if habit_form.is_valid():
                habit_data = {k: v for k, v in habit_form.cleaned_data.items()}
                habit_list = [Habits(**habit_data)]
                if request.POST.get('edit_habit_data') and request.POST.get('personal_history'):
                    if pesonal_his:
                        pesonal_his.habits.pop(int(request.POST.get('habit_index_no'))-1)
                        pesonal_his.habits.insert(int(request.POST.get('habit_index_no'))-1, Habits(**habit_data))
                        pesonal_his.save()
                        request.session['success_msg'] = _("Habit details has been updated successfully.")
                elif request.POST.get('add_habit_data') and request.POST.get('personal_history'):
                    if pesonal_his.habits:
                        pesonal_his.habits.extend(habit_list)
                    else:
                        pesonal_his.habits = habit_list
                    pesonal_his.save()
                    request.session['success_msg'] = _("Habit details has added saved successfully.")
                else:
                    CasePersonalHistory.objects.create(case_id=case_id,
                                    habits = habit_list,
                                    diets = None,
                                    evolutionary_history=EvolutionaryHistory())
                    request.session['success_msg'] = _("Habit details has been saved successfully.")
        
        elif ("add_diet_data" in request.POST or 'edit_diet_data' in request.POST) and case_id:
            diet_form = DietsForm(request.POST)
            if diet_form.is_valid():
                diet_data = {k: v for k, v in diet_form.cleaned_data.items()}
                diet_list = [Diets(**diet_data)]
                if request.POST.get('edit_diet_data') and request.POST.get('personal_history'):
                    if pesonal_his:
                        pesonal_his.diets.pop(int(request.POST.get('diet_index_no'))-1)
                        pesonal_his.diets.insert(int(request.POST.get('diet_index_no'))-1, Diets(**diet_data))
                        pesonal_his.save()
                        request.session['success_msg'] = _("Diet details has been updated successfully.")
                elif request.POST.get('add_diet_data') and request.POST.get('personal_history'):
                    if pesonal_his.diets:
                        pesonal_his.diets.extend(diet_list)
                    else:
                        pesonal_his.diets = diet_list
                    pesonal_his.save()
                    request.session['success_msg'] = _("Diet details has been saved successfully.")
                else:
                    CasePersonalHistory.objects.create(case_id=case_id,
                                    habits = None,
                                    diets = diet_list,
                                    evolutionary_history=EvolutionaryHistory())
                    request.session['success_msg'] = _("Diet details has been saved successfully.")
                    
        elif "other_data" in request.POST  and case_id:
            pers_his_form = PersonalHistoryForm(request.POST)
            if pers_his_form.is_valid():
                pers_his_data = {k: v for k, v in pers_his_form.cleaned_data.items()}
                if request.POST.get('personal_history'):
                    if pesonal_his:
                        pesonal_his.case_patient_economy_status = request.POST.get('case_patient_economy_status')
                        pesonal_his.hobbies = request.POST.get('hobbies')
                        pesonal_his.evolutionary_history = EvolutionaryHistory(
                                        evl_history = request.POST.getlist('evl_history'),
                                        evl_history_others = request.POST.get('evl_history_others'))
                        pesonal_his.save()
                    request.session['success_msg'] = _("Others details has been updated successfully.")
                else:
                    CasePersonalHistory.objects.create(case_id=case_id,
                                    habits = None,
                                    diets = None,
                                    evolutionary_history = EvolutionaryHistory(
                                        evl_history = request.POST.getlist('evl_history'),
                                        evl_history_others = request.POST.get('evl_history_others')),
                                    **pers_his_data)
                    request.session['success_msg'] = _("Others details has been saved successfully.")
        elif request.POST.get("delete_type") == "Habit":
            pesonal_his.habits.pop(int(request.POST.get('index_no'))-1)
            pesonal_his.save()
            request.session['success_msg'] = _("Habit details has been deleted successfully.")
               
        elif request.POST.get("delete_type") == 'Diet':
            pesonal_his.diets.pop(int(request.POST.get('index_no'))-1)
            pesonal_his.save()
            request.session['success_msg'] = _("Diet details has been deleted successfully.")
        elif request.POST.get("delete_type") == 'Others':
            pesonal_his.case_patient_economy_status = None
            pesonal_his.hobbies = None
            pesonal_his.evolutionary_history = EvolutionaryHistory(
                                        evl_history = None,
                                        evl_history_others = None)
            pesonal_his.save()
            request.session['success_msg'] = _("Others Details has been deleted successfully.")
    
        if case_id:
            return HttpResponseRedirect(reverse_lazy('case_history:personal_history', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:personal_history'))
"""Personal history functionality - ends here"""

# """Physical general functionality - starts here"""
# @login_required
# def physical_general(request, case_id=None):
#     if request.method == 'GET':
#         success = request.session.pop('success_msg', None)
#         case_record = CasePhysicalGeneral.objects.filter(case_id=case_id)
#         physical_type = PhysicalGeneralType.objects.filter(status__status_name='Active').order_by('gen_type_name')
#         physical_general_mst = PhysicalGeneralMaster.objects.filter(status__status_name='Active').order_by('gen_type__gen_type_name')
#         return render(request,'case_history/physical_general.html',{'case_id':case_id,
#                                                                     'physical_type':physical_type,
#                                                                     'add_physcial_general':'add_physcial_general',
#                                                                     'case_record':case_record,
#                                                                     'physical_general_mst':physical_general_mst,
#                                                                     'success_msg':success,
#                                                                     'activeTab': request.GET.get('activeTab')})
# 
#     elif request.method == 'POST':
#         postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^gentype_\d+', key)]
#         if postdata_keys:
#             for each in postdata_keys:
#                 if  request.POST.get("gentype_%s" % each, None):
#                     phygen_value = request.POST.get("gentype_%s" % each, None)
#                 else:
#                     phygen_value = None
#                 if  request.POST.get("generalmast_%s" % each, None):
#                     general_mastr_id = request.POST.get("generalmast_%s" % each, None)
#                 else:
#                     general_mastr_id = None
#                 try:
#                     physcial_gnrl = CasePhysicalGeneral.objects.get(case_id=case_id,hab_id=general_mastr_id).id
#                 except:
#                     physcial_gnrl = None
#                 if physcial_gnrl:
#                     case_genral_value = CasePhysicalGeneral.objects.filter(id=physcial_gnrl).update(
#                                                                        hab_id=general_mastr_id,
#                                                                        phygen_value=phygen_value)
#                 else:
#                     case_genral_value = CasePhysicalGeneral.objects.create(case_id=case_id,
#                                                                        hab_id=general_mastr_id,
#                                                                        phygen_value=phygen_value)
#             #Save the case status history
#             keep_case_status_history(case_id)
#             request.session['success_msg'] = _("Physical General has been saved successfully.")
#         return HttpResponseRedirect(reverse_lazy('case_history:physical_general', args=[case_id]))
# """Physical general functionality - ends here"""

"""Mental general functionality - starts here"""
@login_required
def mental_general(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        #Getting the dynamic record based on the requested Case ID.
        try:
            case_record = CaseMentalGeneral.objects.get(case_id=case_id)
        except:
            case_record = None
            
        if request.GET.get('mental_index'):
            form = MentalGeneralsForm(instance = case_record.mental_generals[int(request.GET.get('mental_index'))-1])
        else:
            form = MentalGeneralsForm()
        
        #For edit/update case
        return render(request,'case_history/mental_general.html',{'form':form,
                                                                  'success_note':success,
                                                                  'case_record':case_record,
                                                                  'case_id':case_id,
                                                                  'mental_details':request.GET.get('mental_index'),
                                                                  })
    elif request.method == 'POST':
        form = MentalGeneralsForm(request.POST)
        try:
            ment_obj = CaseMentalGeneral.objects.get(case_id=case_id)
        except:
            ment_obj = None
        if form.is_valid() and case_id:
            data = {k: v for k, v in form.cleaned_data.items()}
            if request.POST.get('mental_details'):
                ment_obj.mental_generals.pop(int(request.POST.get('mental_details'))-1)
                ment_obj.mental_generals.insert(int(request.POST.get('mental_details'))-1 , MentalGenerals(**data))
                ment_obj.save()
                request.session['success_msg'] = _("Mental General details has been updated successfully.")
            elif ment_obj:
                ment_obj.mental_generals.extend([MentalGenerals(**data)])
                ment_obj.save()
                request.session['success_msg'] = _("Mental General details has been saved successfully.")
            else:
                CaseMentalGeneral.objects.create(case_id=case_id,mental_generals=[MentalGenerals(**data)])
                request.session['success_msg'] = _("Mental General has details been saved successfully.")
        elif request.POST.get("delete_mental_general"):
            ment_obj.mental_generals.pop(int(request.POST.get('index_no'))-1)
            ment_obj.save()
            request.session['success_msg'] = _("Mental General details has been deleted successfully.")
        else:
            request.session['success_msg'] = _("Please check the all mandatory fields carefully.")
        
        if case_id:
            return HttpResponseRedirect(reverse_lazy('case_history:mental_general', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:mental_general'))
"""Mental general functionality - ends here"""

"""Past general functionality - starts here"""
@login_required
def past_general(request, case_id=None):
    if request.method == 'GET':
        case_past_record =  past_supression_index = past_histry_form = None
        birth_history_data = delivery_his_data = mthr_helth_data = breast_feeding_data = None
        try:
            case_past_record = CasePastHistory.objects.get(case_id=case_id)
        except:
            case_past_record = None
            
        if case_past_record:
            if case_past_record.history_of_children.birth_history.prematurity or case_past_record.history_of_children.birth_history.birth_injuries or case_past_record.history_of_children.birth_history.birth_weight or case_past_record.history_of_children.birth_history.neonatal_complaints:
                birth_history_data = 'birth_history'
            if case_past_record.history_of_children.delivery_his_details.delivery_history or case_past_record.history_of_children.delivery_his_details.premature_others:
                delivery_his_data = 'delivery_his_details'
            if case_past_record.history_of_children.mthr_helth_history.mthr_helth_during_preg or case_past_record.history_of_children.mthr_helth_history.mthr_helth_during_preg_oth:
                mthr_helth_data = 'mthr_helth_history'
            if case_past_record.history_of_children.breast_feeding_history.duration or case_past_record.history_of_children.breast_feeding_history.mothers_milk:
                breast_feeding_data = 'breast_feeding_history'

        if case_past_record:
            birth_histry = BirthHistoryForm(instance = case_past_record.history_of_children.birth_history)
            delivery_hsty = DeliveryHisDetailsForm(instance = case_past_record.history_of_children.delivery_his_details)
            mother_health = MotherHealthHistoryForm(instance = case_past_record.history_of_children.mthr_helth_history)
            breast_feeding = BreastFeedingHistoryForm(instance = case_past_record.history_of_children.breast_feeding_history)
            if request.GET.get('past_general_index_no'):
                past_histry_form = PastHistoryForm(instance = case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1])
            else:
                past_histry_form = PastHistoryForm(instance = case_past_record)
        else:
            birth_histry = BirthHistoryForm()
            delivery_hsty = DeliveryHisDetailsForm()
            mother_health = MotherHealthHistoryForm()
            breast_feeding = BreastFeedingHistoryForm()
            past_histry_form = PastHistoryForm()
            histry_form = HistoryOfSuppressionForm()
        if request.GET.get('past_supression_index_no'):
            past_supression_index = int(request.GET.get('past_supression_index_no'))
        dis_any_index = dis_being_index= dis_bronch_index= dis_tuber_index=dis_others_index = dis_cancer_index = dis_stds_index =  dis_Jaundice_index = dis_Measles_index = dis_Eczema_index = dis_Chickenpox_index =None
        if case_past_record:
            for index, item in enumerate(case_past_record.past_history, start=1):
                    if item.dis_name == 'Any recurrent infections':
                        dis_any_index = index
                    if item.dis_name == 'Bronchial Asthma':
                        dis_bronch_index = index
                    if item.dis_name == 'Tuberculosis':
                        dis_tuber_index = index
                    if item.dis_name == 'Chickenpox':
                        dis_Chickenpox_index = index
                    if item.dis_name == 'Eczema':
                        dis_Eczema_index = index
                    if item.dis_name == 'Measles':
                        dis_Measles_index = index
                    if item.dis_name == 'Jaundice':
                        dis_Jaundice_index = index
                    if item.dis_name == 'STDs':
                        dis_stds_index = index
                    if item.dis_name == 'Cancer':
                        dis_cancer_index = index
                    if item.dis_name == 'benign tumors/growths':
                        dis_being_index = index
                    if item.dis_name == 'Others':
                        dis_others_index = index
                
        
        
        success_msg = request.session.pop('success_msg', None)
        past_history_save = request.session.pop('past_history_save', None)
        his_child_save = request.session.pop('his_child_save', None)
        past_histry_empty_form = PastHistoryForm()
        return render(request,'case_history/past_general.html',{
                                                                'birth_histry':birth_histry,
                                                                'delivery_hsty':delivery_hsty,
                                                                'mother_health':mother_health,
                                                                'breast_feeding':breast_feeding,
                                                                'case_past_record':case_past_record,
                                                                'case_id':case_id,
                                                                'past_histry_form':past_histry_form,
                                                                'past_general_index_no':request.GET.get('past_general_index_no'),
                                                                'past_supression_index_no':past_supression_index,
                                                                'injuries_edit':request.GET.get('injuries_edit'),
                                                                'accident_edit':request.GET.get('accident_edit'),
                                                                'surgery_edit':request.GET.get('surgery_edit'),
                                                                'birt_history':request.GET.get('birt_history'),
                                                                'delivery_history':request.GET.get('delivery_history'),
                                                                'mthr_helth_history':request.GET.get('mthr_helth_history'),
                                                                'breast_feeding_history':request.GET.get('breast_feeding_history'),
                                                                'success_note':success_msg,
                                                                'past_history':request.GET.get('past_history'),
                                                                'past_histry_empty_form':past_histry_empty_form,
                                                                'year_of_onset':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].year_of_onset if request.GET.get('past_general_index_no') else None,
                                                                'age_of_onset':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].age_of_onset if request.GET.get('past_general_index_no') else None,
                                                                'treatment_histoy':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].treatment_histoy if request.GET.get('past_general_index_no') else None,
                                                                'outcome':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].outcome if request.GET.get('past_general_index_no') else None,
                                                                'reccurance':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].reccurance if request.GET.get('past_general_index_no') else None,
                                                                'other_disease':case_past_record.past_history[int(request.GET.get('past_general_index_no'))-1].other_disease if request.GET.get('past_general_index_no') else None,
                                                                'past_history_save':past_history_save,
                                                                'birth_history_data':birth_history_data,
                                                                'delivery_his_data':delivery_his_data,
                                                                'mthr_helth_data':mthr_helth_data,
                                                                'breast_feeding_data':breast_feeding_data,
                                                                'his_child_save':his_child_save,
                                                                'dis_any_index':dis_any_index,
                                                                'dis_bronch_index':dis_bronch_index,
                                                                'dis_tuber_index':dis_tuber_index,
                                                                'dis_others_index':dis_others_index,
                                                                'dis_being_index':dis_being_index,
                                                                'dis_cancer_index':dis_cancer_index,
                                                                'dis_stds_index':dis_stds_index,
                                                                'dis_Jaundice_index':dis_Jaundice_index,
                                                                'dis_Measles_index':dis_Measles_index,
                                                                'dis_Eczema_index':dis_Eczema_index,
                                                                'dis_Chickenpox_index':dis_Chickenpox_index
                                                                })
 
 
    elif request.method == 'POST':
        
        if case_id:
            if CasePastHistory.objects.filter(case_id = request.POST.get('case_id_id')).exists():
                case_hsiry = CasePastHistory.objects.get(case_id = request.POST.get('case_id_id'))
            else:
                case_hsiry = CasePastHistory(
                    case_id = request.POST.get('case_id_id'),
                    past_history= None,
                    history_of_suppression=None,
                    injuries = None,
                    accidents = None,
                    surgery = None,
                    history_of_children = HistoryOfChildren(
                        birth_history = BirthHistory(),
                        delivery_his_details = DeliveryHisDetails(),
                        mthr_helth_history = MotherHealthHistory(),
                        breast_feeding_history = BreastFeedingHistory(),
                        )
                    )
                case_hsiry.save()
            if request.POST.get('delete_present_complaint'):
                if request.POST.get('field_name') == 'breast_feeding_history':
                    case_hsiry.history_of_children.breast_feeding_history=BreastFeedingHistory()
                    case_hsiry.save()
                    request.session['success_msg'] = _("Breast Feeding History details has been deleted successfully.")
                elif request.POST.get('field_name') == 'birth_history':
                    case_hsiry.history_of_children.birth_history=BirthHistory()
                    case_hsiry.save()
                    request.session['success_msg'] = _("Birth History details has been  deleted successfully.")
                elif request.POST.get('field_name') == 'delivery_history':
                    case_hsiry.history_of_children.delivery_his_details=DeliveryHisDetails()
                    case_hsiry.save()
                    request.session['success_msg'] = _("Delivery History details Details has been deleted successfully.")
                elif request.POST.get('field_name') == 'mthr_helth_history':
                    case_hsiry.history_of_children.mthr_helth_history=MotherHealthHistory()
                    case_hsiry.save()
                    request.session['success_msg'] = _("Mother Health History details has been deleted successfully.")
                elif request.POST.get('field_name') == 'injuries':
                    case_hsiry.injuries = None
                    case_hsiry.save()
                    request.session['success_msg'] = _("Injuries details has been deleted successfully.")
                elif request.POST.get('field_name') == 'accidents':
                    case_hsiry.accidents = None
                    case_hsiry.save()
                    request.session['success_msg'] = _("Accidents details has been deleted successfully.")
                elif request.POST.get('field_name') == 'surgery':
                    case_hsiry.surgery = None
                    case_hsiry.save()
                    request.session['success_msg'] = _("Surgery details has been deleted successfully.")
                elif request.POST.get('field_name') == 'history_suppression':
                    case_hsiry.history_of_suppression.pop(int(request.POST.get('indeex_no_field'))-1)
                    case_hsiry.save()
                    request.session['success_msg'] = _("History Suppression details has been deleted successfully.")
                elif request.POST.get('field_name') == 'past_history':
                    case_hsiry.past_history.pop(int(request.POST.get('indeex_no_field'))-1)
                    case_hsiry.save()
                    request.session['success_msg'] = _("Past History details has been deleted successfully.")
                 
            elif "birth_histry" in request.POST and request.POST.get('case_id_id'):
                birth_hstry_form = BirthHistoryForm(request.POST)
                if birth_hstry_form.is_valid():
                    birth_hist_data = {k: v for k, v in birth_hstry_form.cleaned_data.items()}
                    case_hsiry.history_of_children.birth_history = BirthHistory(**birth_hist_data)
                    case_hsiry.save()
                    request.session['his_child_save'] = 'his_child_save'
                    request.session['success_msg'] = _("History in children details has been saved successfully.")
    
            elif "delivery_history_id" in request.POST and request.POST.get('case_id_id'):
                delivery_hsry_form = DeliveryHisDetailsForm(request.POST)
                if delivery_hsry_form.is_valid():
                    delivery_hist_data = {k: v for k, v in delivery_hsry_form.cleaned_data.items()}
                    case_hsiry.history_of_children.delivery_his_details = DeliveryHisDetails(**delivery_hist_data)
                    case_hsiry.save()
                    request.session['his_child_save'] = 'his_child_save'
                    request.session['success_msg'] = _("History in children details has been saved successfully.")
    
            elif "mother_value" in request.POST and request.POST.get('case_id_id'):
                mother_health_form = MotherHealthHistoryForm(request.POST)
                if mother_health_form.is_valid():
                    mother_health_data = {k: v for k, v in mother_health_form.cleaned_data.items()}
                    case_hsiry.history_of_children.mthr_helth_history = MotherHealthHistory(**mother_health_data)
                    case_hsiry.save()
                    request.session['his_child_save'] = 'his_child_save'
                    request.session['success_msg'] = _("History in children details has been saved successfully.")
    
            elif "breast_feeding" in request.POST and request.POST.get('case_id_id'):
                breast_feeding_form = BreastFeedingHistoryForm(request.POST)
                if breast_feeding_form.is_valid():
                    breast_feeding_data = {k: v for k, v in breast_feeding_form.cleaned_data.items()}
                    case_hsiry.history_of_children.breast_feeding_history = BreastFeedingHistory(**breast_feeding_data)
                    case_hsiry.save()
                    request.session['his_child_save'] = 'his_child_save'
                    request.session['success_msg'] = _("History in children details has been saved successfully.")
    
            elif "case_histry_dtl_val" in request.POST and request.POST.get('case_id_id'):
                if request.POST.get('injuries_val'):
                    case_hsiry.injuries = request.POST.get('injuries_val') 
                    request.session['success_msg'] = _("Injuries details has been saved successfully.")   
                else:
                    case_hsiry.injuries 
                if request.POST.get('accident_val'):
                    case_hsiry.accidents = request.POST.get('accident_val') 
                    request.session['success_msg'] = _("Accidents details has been saved successfully.")  
                else:
                    case_hsiry.accidents
                if request.POST.get('surgery_val'):
                    case_hsiry.surgery = request.POST.get('surgery_val')   
                    request.session['success_msg'] = _("Surgery details has been saved successfully.")   
                else:
                    case_hsiry.surgery
                case_hsiry.save()
            elif 'past_history_supression' in request.POST and request.POST.get('case_id_id'):
                try:
                    disese_id = DiseaseMaster.objects.get(dis_name=request.POST.get('disease_name'))
                except:
                    disese_id = None
                a_list = None
                if disese_id:
                    a_list = [PastHistory(dis_name=request.POST.get('disease_name'),
                                    icd_code = disese_id.dis_icd_code if disese_id.dis_icd_code else None ,
                                    year_of_onset=request.POST.get('year_of_onset'),
                                    age_of_onset=request.POST.get('age_of_onset'),
                                    treatment_histoy=request.POST.get('treatment_histoy'),
                                    outcome=request.POST.get('outcome'),
                                    reccurance=request.POST.get('reccurance'),
                                    other_disease=request.POST.get('other_disease'),
                                     )]
                    if request.POST.get('past_histr_index') and case_hsiry.past_history[int(request.POST.get('past_histr_index'))-1].dis_name == request.POST.get('disease_name'):
                        case_hsiry.past_history.pop(int(request.POST.get('past_histr_index'))-1)
                        case_hsiry.past_history.insert(int(request.POST.get('past_histr_index'))-1,PastHistory(dis_name=request.POST.get('disease_name'),
                                        icd_code = disese_id.dis_icd_code if disese_id.dis_icd_code else None,
                                        year_of_onset=request.POST.get('year_of_onset'),
                                        age_of_onset=request.POST.get('age_of_onset'),
                                        treatment_histoy=request.POST.get('treatment_histoy'),
                                        outcome=request.POST.get('outcome'),
                                        reccurance=request.POST.get('reccurance'),
                                        other_disease=request.POST.get('other_disease'),
                                         ))
                        case_hsiry.save()
                    elif case_hsiry.past_history :
                        case_hsiry.past_history.extend(a_list) 
                        case_hsiry.save()
                    else:
                        case_hsiry.past_history = a_list
                        case_hsiry.save()
                    request.session['past_history_save'] = 'past_history_save'
                    request.session['success_msg'] = _("Past History details has been saved successfully.")  
            elif 'history_supression' in request.POST and request.POST.get('case_id_id'):
                data_list=data_as_past_supression_list(request.POST)
                counter = 0
                for i in data_list:
                    if request.POST.get('past_supression_idex'):
                        case_hsiry.history_of_suppression.pop(int(request.POST.get('past_supression_idex'))-1)
                        case_hsiry.history_of_suppression.insert(int(request.POST.get('past_supression_idex'))-1,HistoryOfSuppression(type_of_suppression=i[0],
                                                      year_of_suppression=i[1],
                                                      age_of_suppression=i[2],
                                                      aetiology=i[3],
                                                      other_information=i[4],
                                                    ))
                        case_hsiry.save()
                        request.session['success_msg'] = _("History of Suppression details has been saved successfully.")  
                    elif case_hsiry.history_of_suppression:
                        case_hsiry.history_of_suppression.extend([HistoryOfSuppression(type_of_suppression=i[0],
                                                          year_of_suppression=i[1],
                                                          age_of_suppression=i[2],
                                                          aetiology=i[3],
                                                          other_information=i[4],
                                                    )]) 
                        case_hsiry.save()
                    else:
                        case_hsiry.history_of_suppression= ([HistoryOfSuppression(type_of_suppression=i[0],
                                                              year_of_suppression=i[1],
                                                              age_of_suppression=i[2],
                                                              aetiology=i[3],
                                                              other_information=i[4],
                                                        )]) 
                        case_hsiry.save()
                        
                        request.session['success_msg'] = _("History of Suppression details has been saved successfully.")  
            return HttpResponseRedirect(reverse_lazy('case_history:past_general',args=[request.POST.get('case_id_id')]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:past_general'))
"""Past general functionality - ends here"""

"""Family history functionality - starts here"""
@login_required
def family_history(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        relation_list = ['Father','Mother','Brother','Sister','Paternal Grandfather',
                         'Paternal Grandmother', 'Maternal Grandfather', 'Maternal Grandmother']
        try:
            family_hist = CaseFamilyHistory.objects.get(case_id=case_id)
        except:
            family_hist = None
        
        if request.GET.get('relation_index_no'):
            relation_details = family_hist.family_history[int(request.GET.get('relation_index_no'))-1]
            
        else:
            relation_details = None
                        
        return render(request,'case_history/family_history.html', {'case_id':case_id,
                                                                   'success_note':success,
                                                                   'family_hist':family_hist,
                                                                   'relation_index_no':request.GET.get('relation_index_no'),
                                                                   'relation_details':relation_details,
                                                                   'relation_list':relation_list,
                                                                })
    if request.method == 'POST':
        if CaseFamilyHistory.objects.filter(case_id=case_id).exists():
            fam_obj = CaseFamilyHistory.objects.get(case_id=case_id)
        else:
            fam_obj = CaseFamilyHistory(case_id = case_id,
                                        family_history = None)
            fam_obj.save()
        dis_pastlist = []
        dis_presentlist = []
        past_dis = list(map(str,request.POST.getlist('past_disease[]')))
        present_dis = list(map(str,request.POST.getlist('present_disease[]')))
            
        for i in past_dis:
            dis_icd_names = DiseaseMaster.objects.get(id=i)
            other_list = [Diseases(disease=DiseaseMaster.objects.get(id=i),dis_icd_code=dis_icd_names.dis_icd_code)]
            dis_pastlist.extend(other_list)
        
        for i in present_dis:
            dis_icd_name = DiseaseMaster.objects.get(id=i)
            other_list = [PresentDiseases(present_disease=DiseaseMaster.objects.get(id=i),present_dis_icd_code=dis_icd_name.dis_icd_code)]
            dis_presentlist.extend(other_list)
            
        fam_coll = FamilyHistory(diseases=dis_pastlist,
                                present_diseases = dis_presentlist,
                                accidents = request.POST.get('accident'),
                                alive_dead = request.POST.get('alive_dead'),
                                relation = request.POST.get('relation_name'),)
         
        if not case_id:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:family_history'))   
        
        elif 'add_relation_data' in request.POST and case_id:
            relation_name = request.POST.get('relation_name')
            if request.POST.get('relation_index_no'):
                fam_obj.family_history.pop(int(request.POST.get('relation_index_no'))-1)
                fam_obj.family_history.insert(int(request.POST.get('relation_index_no'))-1, fam_coll)
            elif fam_obj.family_history and request.POST.get('add_relation_data'):
                fam_obj.family_history.extend([fam_coll])
            else:
                fam_obj.family_history = [fam_coll]
            fam_obj.save()
            request.session['success_msg'] = relation_name + _(" details has been saved successfully.")
        elif request.POST.get('field_name'):
            field_name = request.POST.get('field_name')
            fam_obj.family_history.pop(int(request.POST.get('index_no'))-1)
            fam_obj.save()
            request.session['success_msg'] = field_name +_(" details has been deleted successfully.")
        return HttpResponseRedirect(reverse_lazy('case_history:family_history', args=[case_id]))
 
"""Family history functionality - ends here"""

"""Gynaecological history functionality - starts here"""
@login_required
def gynaecological_history(request, case_id=None):
    if request.method == 'GET':
        gyno_record = None
        success = request.session.pop('success_msg', None)
        menstrual_save = request.session.pop('menstrual_save', None)
        ho_gyna_surgeries = request.session.pop('ho_gyna_surgeries', None)
        abnormal_dise_sav = request.session.pop('abnormal_dise_sav', None)
        hysterectomy_data = lmp_data = bleeding_data = cycle_data = colour_data = consis_data = odour_data = character_data = dysmen_data = None

        try:
            gyno_record = CaseGynaecologicalHistory.objects.get(case_id=case_id)
            menarche_form = MenarcheForm(instance = gyno_record.menarche)
            menop_form = MenopauseForm(instance = gyno_record.menopause)
            leu_form = LeucorrheaForm(instance = gyno_record.abnormal_discharge.leucorrhea)
            bleed_form = BleedingPerVaginaForm(instance = gyno_record.abnormal_discharge.bleeding_per_vagina)
            hyst_form = HysterectomyForm(instance = gyno_record.ho_gynaecological_surgeries.hysterectomy)
            lmp_form = LmpForm(instance = gyno_record.menstrual_cycle_particulars.lmp)
            bleeding_form = BleedingForm(instance = gyno_record.menstrual_cycle_particulars.bleeding)
            cycle_form = CycleForm(instance = gyno_record.menstrual_cycle_particulars.cycle)
            color_form = ColourForm(instance = gyno_record.menstrual_cycle_particulars.colour)
            consis_form = ConsistencyForm(instance = gyno_record.menstrual_cycle_particulars.consistency)
            odur_form = OdourForm(instance = gyno_record.menstrual_cycle_particulars.odour)
            charact_form = CharacterForm(instance = gyno_record.menstrual_cycle_particulars.character)
            dysm_form = DysmenorrhoeaForm(instance = gyno_record.menstrual_cycle_particulars.dysmenorrhoea)
            
        except:
            gyno_record = None
            menarche_form = MenarcheForm()
            leu_form = LeucorrheaForm()
            bleed_form = BleedingPerVaginaForm()
            menop_form = MenopauseForm()
            hyst_form = HysterectomyForm()
            lmp_form = LmpForm()
            bleeding_form = BleedingForm()
            cycle_form = CycleForm()
            color_form = ColourForm()
            consis_form = ConsistencyForm()
            odur_form = OdourForm()
            charact_form = CharacterForm()
            dysm_form = DysmenorrhoeaForm()
        
        
        if gyno_record:
            if gyno_record.menstrual_cycle_particulars.lmp.date:
                lmp_data = 'lmp'
            if gyno_record.menstrual_cycle_particulars.bleeding.days:
                bleeding_data = 'bleeding'
            if gyno_record.menstrual_cycle_particulars.cycle.cycle:
                cycle_data = 'cycle'
            if gyno_record.menstrual_cycle_particulars.colour.colour:
                colour_data = 'colour'
            if gyno_record.menstrual_cycle_particulars.consistency.consistency:
                consis_data = 'consistency'
            if gyno_record.menstrual_cycle_particulars.odour.odour:
                odour_data = 'odour'
            if gyno_record.menstrual_cycle_particulars.character.character:
                character_data = 'character'
            if gyno_record.menstrual_cycle_particulars.dysmenorrhoea.dysmenorrhoea:
                dysmen_data = 'dysmenorrhoea'
            if gyno_record.ho_gynaecological_surgeries.hysterectomy.hysterectomy or gyno_record.ho_gynaecological_surgeries.hysterectomy.reason or gyno_record.ho_gynaecological_surgeries.hysterectomy.age:
                hysterectomy_data = 'hysterectomy'
        if (request.GET.get('other_index_no') or request.GET.get('complaints_index_no') or request.GET.get('contraceptive_index_no')) and gyno_record:
            try:
                oth_form = OthersForm(instance=gyno_record.ho_gynaecological_surgeries.others[int(request.GET.get('other_index_no'))-1])
            except:
                oth_form = OthersForm()
            try:
                compa_form = ComplaintsForm(instance=gyno_record.menstrual_cycle_particulars.complaints[int(request.GET.get('complaints_index_no'))-1])
            except:
                compa_form = ComplaintsForm()
            try:
                contr_form = ContraceptiveMethodsForm(instance=gyno_record.contraceptive_methods[int(request.GET.get('contraceptive_index_no'))-1])
            except:
                contr_form = ContraceptiveMethodsForm()
        else:
            oth_form = OthersForm()
            contr_form = ContraceptiveMethodsForm()
            compa_form = ComplaintsForm()
        return render(request,'case_history/gynaecological_history.html',{
                                                                        'case_id':case_id,
                                                                        'gyno_record':gyno_record,
                                                                        'menarche_form':menarche_form,
                                                                        'leu_form':leu_form,
                                                                        'bleed_form':bleed_form,
                                                                        'menop_form':menop_form,
                                                                        'hyst_form':hyst_form,
                                                                        'oth_form':oth_form,
                                                                        'contr_form':contr_form,
                                                                        'lmp_form':lmp_form,
                                                                        'bleeding_form':bleeding_form,
                                                                        'cycle_form':cycle_form,
                                                                        'color_form':color_form,
                                                                        'consis_form':consis_form,
                                                                        'odur_form':odur_form,
                                                                        'charact_form':charact_form,
                                                                        'dysm_form':dysm_form,
                                                                        'compa_form':compa_form,
                                                                        'success_note':success,
                                                                        'other_index_no':request.GET.get('other_index_no'),
                                                                        'complaints_index_no':request.GET.get('complaints_index_no'),
                                                                        'contraceptive_index_no':request.GET.get('contraceptive_index_no'),
                                                                        'menstrual_save':menstrual_save,
                                                                        'ho_gyna_surgeries':ho_gyna_surgeries,
                                                                        'abnormal_dise_sav':abnormal_dise_sav,
                                                                        'lmp_data':lmp_data,
                                                                        'bleeding_data':bleeding_data,
                                                                        'cycle_data':cycle_data,
                                                                        'colour_data':colour_data,
                                                                        'consis_data':consis_data,
                                                                        'odour_data':odour_data,
                                                                        'character_data':character_data,
                                                                        'dysmen_data':dysmen_data,
                                                                        'hysterectomy_data':hysterectomy_data,
                                                                        
                                                                    })
# 
    elif request.method == 'POST':
        if case_id:
            if CaseGynaecologicalHistory.objects.filter(case_id=case_id).exists():
                case_gyno_record = CaseGynaecologicalHistory.objects.get(case_id=case_id)
            else:
                case_gyno_record = CaseGynaecologicalHistory(
                        case_id = case_id,
                        menarche = Menarche(),
                        menstrual_cycle_particulars = MenstrualCycleParticulars(
                            lmp = Lmp(),
                            bleeding = Bleeding(),
                            cycle = Cycle(),
                            colour = Colour(),
                            consistency = Consistency(),
                            odour = Odour(),
                            character = Character(),
                            dysmenorrhoea = Dysmenorrhoea(),
                            complaints = None
                        ),
                        abnormal_discharge = AbnormalDischarge(
                            leucorrhea = Leucorrhea(),
                            bleeding_per_vagina = BleedingPerVagina()
                        ),
                        menopause = Menopause(),
                        ho_gynaecological_surgeries = HoGynaecologicalSurgeries(
                            hysterectomy = Hysterectomy(),
                            others = None
                        ),
                        contraceptive_methods = None
                    )
#             case_gyno_record.save()
#       Delete Condition Starts
        
            
            if request.POST.get('delete_entity'):
                if request.POST.get('field_name') == 'menarche':
                    case_gyno_record.menarche = Menarche()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Menarche details has been deleted successfully.")
                elif request.POST.get('field_name') == 'leucorrhea':
                    case_gyno_record.abnormal_discharge.leucorrhea = Leucorrhea()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Leucorrhea details has been deleted successfully.")
                elif request.POST.get('field_name') == 'bleeding_per_vagina':
                    case_gyno_record.abnormal_discharge.bleeding_per_vagina = BleedingPerVagina()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Bleeding Per Vagina details has been deleted successfully.")
                elif request.POST.get('field_name') == 'menopause':
                    case_gyno_record.menopause = Menopause()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Menopause details has been deleted successfully.")
                elif request.POST.get('field_name') == 'hysterectomy':
                    case_gyno_record.ho_gynaecological_surgeries.hysterectomy = Hysterectomy()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Hysterectomyel details has been deleted successfully.")
                elif request.POST.get('field_name') == 'others':
                    case_gyno_record.ho_gynaecological_surgeries.others.pop(int(request.POST.get('index_no'))-1)
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Others details has been deleted successfully.")
                elif request.POST.get('field_name') == 'contraceptive_methods':
                    case_gyno_record.contraceptive_methods.pop(int(request.POST.get('index_no'))-1)
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Contraceptive Method details has been deleted successfully.")
                elif request.POST.get('field_name') == 'lmp':
                    case_gyno_record.menstrual_cycle_particulars.lmp = Lmp()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("LMP details has been deleted successfully.")
                elif request.POST.get('field_name') == 'bleeding':
                    case_gyno_record.menstrual_cycle_particulars.bleeding = Bleeding()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Bleeding details has been deleted successfully.")
                elif request.POST.get('field_name') == 'cycle':
                    case_gyno_record.menstrual_cycle_particulars.cycle = Cycle()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Cycle details has been deleted successfully.")
                elif request.POST.get('field_name') == 'colour':
                    case_gyno_record.menstrual_cycle_particulars.colour = Colour()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Colour details has been deleted successfully.")
                elif request.POST.get('field_name') == 'consistency':
                    case_gyno_record.menstrual_cycle_particulars.consistency = Consistency()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Consistency details has been deleted successfully.")
                elif request.POST.get('field_name') == 'odour':
                    case_gyno_record.menstrual_cycle_particulars.odour = Odour()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Odur details has been deleted successfully.")
                elif request.POST.get('field_name') == 'character':
                    case_gyno_record.menstrual_cycle_particulars.character = Character()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Character details has been deleted successfully.")
                elif request.POST.get('field_name') == 'dysmenorrhoea':
                    case_gyno_record.menstrual_cycle_particulars.dysmenorrhoea = Dysmenorrhoea()
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Dysmenorrhoea details has been deleted successfully.")
                elif request.POST.get('field_name') == 'complaints':
                    case_gyno_record.menstrual_cycle_particulars.complaints.pop(int(request.POST.get('index_no'))-1)
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Complaints details has been deleted successfully.")
    #       Delete Conditions Ends
            elif "menarche" in request.POST and case_id:
                menarche_form = MenarcheForm(request.POST)
                if menarche_form.is_valid():
                    menarche_data = {k: v for k, v in menarche_form.cleaned_data.items()}
                    case_gyno_record.menarche = Menarche(**menarche_data)
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Menarche details has been saved successfully.")
            elif "menopause" in request.POST and case_id:
                menop_form = MenopauseForm(request.POST)
                if menop_form.is_valid():
                    menop_data = {k: v for k, v in menop_form.cleaned_data.items()}
                    case_gyno_record.menopause = Menopause(age=request.POST.get('age') if request.POST.get('age') else None,
                                    associated_complaints=request.POST.get('associated_compl_values'))
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Menopause details has been saved successfully.")
            elif "contraceptive_methods" in request.POST and case_id:
                contr_form = ContraceptiveMethodsForm(request.POST)
                if contr_form.is_valid():
                    contr_data = {k: v for k, v in contr_form.cleaned_data.items()}
                    if case_gyno_record and request.POST.get('contraceptive_index_no'):
                        case_gyno_record.contraceptive_methods.pop(int(request.POST.get('contraceptive_index_no'))-1)
                        case_gyno_record.contraceptive_methods.insert(int(request.POST.get('contraceptive_index_no'))-1, ContraceptiveMethods(**contr_data))
                    elif case_gyno_record.contraceptive_methods:
                        case_gyno_record.contraceptive_methods.extend([ContraceptiveMethods(**contr_data)])
                    else:
                        case_gyno_record.contraceptive_methods = [ContraceptiveMethods(**contr_data)]
                    case_gyno_record.save()
                    request.session['success_msg'] = _("Contraceptive Method details has been saved successfully.")
            elif "abnormal_discharge_leucorrhea" in request.POST and case_id:    
                leu_form = LeucorrheaForm(request.POST)
                if leu_form.is_valid():
                    leu_data = {k: v for k, v in leu_form.cleaned_data.items()}
                    case_gyno_record.abnormal_discharge.leucorrhea = Leucorrhea(**leu_data)
                    case_gyno_record.save()
                    request.session['abnormal_dise_sav'] = 'abnormal_dise_sav'
                    request.session['success_msg'] = _("Abnormal Discharge details has been saved successfully.")
            elif "abnormal_discharge_bleeding" in request.POST and case_id:
                bleed_form = BleedingPerVaginaForm(request.POST)
                if bleed_form.is_valid():
                    bleed_data = {k: v for k, v in bleed_form.cleaned_data.items()}
                    case_gyno_record.abnormal_discharge.bleeding_per_vagina = BleedingPerVagina(**bleed_data)
                    case_gyno_record.save()
                    request.session['abnormal_dise_sav'] = 'abnormal_dise_sav'
                    request.session['success_msg'] = _("Abnormal Discharge details has been saved successfully.")
            elif "ho_gynaecological_surgeries_hysterectomy" in request.POST and case_id:
                hyst_form = HysterectomyForm(request.POST)
                if hyst_form.is_valid():
                    hyst_data = {k: v for k, v in hyst_form.cleaned_data.items()}
                    case_gyno_record.ho_gynaecological_surgeries.hysterectomy = Hysterectomy(**hyst_data)
                    case_gyno_record.save()
                    request.session['ho_gyna_surgeries'] = 'ho_gynaecological_surgeries_hysterectomy'
                    request.session['success_msg'] = _("H/O Gynaecological Surgeries details has been saved successfully.")
            elif "ho_gynaecological_surgeries_other" in request.POST and case_id:
                oth_form = OthersForm(request.POST)
                if oth_form.is_valid():
                    oth_data = {k: v for k, v in oth_form.cleaned_data.items()}
                    if case_gyno_record and request.POST.get('other_index_no'):
                        case_gyno_record.ho_gynaecological_surgeries.others.pop(int(request.POST.get('other_index_no'))-1)
                        case_gyno_record.ho_gynaecological_surgeries.others.insert(int(request.POST.get('other_index_no'))-1, Others(**oth_data))
                    elif case_gyno_record.ho_gynaecological_surgeries.others:
                        case_gyno_record.ho_gynaecological_surgeries.others.extend([Others(**oth_data)])
                    else:
                        case_gyno_record.ho_gynaecological_surgeries.others = [Others(**oth_data)]
                    case_gyno_record.save()
                    request.session['ho_gyna_surgeries'] = 'ho_gynaecological_surgeries_other'
                    request.session['success_msg'] = _("H/O Gynaecological Surgeries  details has been saved successfully.")
            elif "lmp_form" in request.POST and case_id:
                lmp_form = LmpForm(request.POST)
                if lmp_form.is_valid():
                    lmp_data = {k: v for k, v in lmp_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.lmp = Lmp(**lmp_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "bleeding_form" in request.POST and case_id:
                bleeding_form = BleedingForm(request.POST)
                if bleeding_form.is_valid():
                    bleeding_data = {k: v for k, v in bleeding_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.bleeding = Bleeding(**bleeding_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "cycle_form" in request.POST and case_id:
                cycle_form = CycleForm(request.POST)
                if cycle_form.is_valid():
                    cycle_data = {k: v for k, v in cycle_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.cycle = Cycle(**cycle_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "color_form" in request.POST and case_id:
                color_form = ColourForm(request.POST)
                if color_form.is_valid():
                    color_data = {k: v for k, v in color_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.colour = Colour(**color_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "consis_form" in request.POST and case_id:
                consis_form = ConsistencyForm(request.POST)
                if consis_form.is_valid():
                    consis_data = {k: v for k, v in consis_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.consistency = Consistency(**consis_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "odur_form" in request.POST and case_id:
                odur_form = OdourForm(request.POST)
                if odur_form.is_valid():
                    odur_data = {k: v for k, v in odur_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.odour = Odour(**odur_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "charact_form" in request.POST and case_id:
                charact_form = CharacterForm(request.POST)
                if charact_form.is_valid():
                    charact_data = {k: v for k, v in charact_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.character = Character(**charact_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "dysm_form" in request.POST and case_id:
                dysm_form = DysmenorrhoeaForm(request.POST)
                if dysm_form.is_valid():
                    dysm_data = {k: v for k, v in dysm_form.cleaned_data.items()}
                    case_gyno_record.menstrual_cycle_particulars.dysmenorrhoea = Dysmenorrhoea(**dysm_data)
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            elif "compa_form" in request.POST and case_id:
                compa_form = ComplaintsForm(request.POST)
                if compa_form.is_valid():
                    compa_data = {k: v for k, v in compa_form.cleaned_data.items()}
                    if case_gyno_record and request.POST.get('complaints_index_no'):
                        case_gyno_record.menstrual_cycle_particulars.complaints.pop(int(request.POST.get('complaints_index_no'))-1)
                        case_gyno_record.menstrual_cycle_particulars.complaints.insert(int(request.POST.get('complaints_index_no'))-1, Complaints(**compa_data))
                    elif case_gyno_record.menstrual_cycle_particulars.complaints:
                        case_gyno_record.menstrual_cycle_particulars.complaints.extend([Complaints(**compa_data)])
                    else:
                        case_gyno_record.menstrual_cycle_particulars.complaints = [Complaints(**compa_data)]
                    case_gyno_record.save()
                    request.session['menstrual_save'] = 'menstrual_cycle_particulars'
                    request.session['success_msg'] = _("Menstrual Cycle Particulars details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:gynaecological_history', args=[case_id]))  
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:gynaecological_history'))  
"""Gynaecological history functionality - Ends Here"""

"""Obstreric history functionality - Start here"""
def obstreric_history(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg',None)
        obs_his_save = request.session.pop('obs_his_save',None)
        save_index_no = request.session.pop('save_index_no',None)
        antenatal_data = pregnancy_index_no = None
        try:
            case_obs_his = CaseObstetricHistory.objects.get(case_id = case_id)
        except:
            case_obs_his = None
        
        try:
            gravida_data = case_obs_his.previous_pregnancies[0]
            para_data = case_obs_his.previous_pregnancies[1]
            abortion_data = case_obs_his.previous_pregnancies[2]
            stillbirth_data = case_obs_his.previous_pregnancies[3]
            living_data = case_obs_his.previous_pregnancies[4]
        except:
            gravida_data = None
            para_data = None
            abortion_data = None
            stillbirth_data = None
            living_data = None
        if request.GET.get('pregnancy_index_no'):
            pregnancy_index_no = request.GET.get('pregnancy_index_no')
        elif save_index_no :
            pregnancy_index_no = save_index_no
        if (save_index_no or request.GET.get('pregnancy_index_no') or request.GET.get('pre_preg_index_no') or request.GET.get('antenatal_index_no') or request.GET.get('postnatal_index_no') or request.GET.get('child_index_no')) and case_obs_his:
            if request.GET.get('pregnancy_index_no'):
                index = request.GET.get('pregnancy_index_no')
            elif request.GET.get('antenatal_index_no'):
                index = request.GET.get('antenatal_index_no')
            elif request.GET.get('postnatal_index_no'):
                index = request.GET.get('postnatal_index_no')
            elif save_index_no:
                index = save_index_no
            try:
                antenatal_data = case_obs_his.pregnancy[int(index)-1].antenatal
                nat_of_lab_form = NatureOfLaborForm(instance = case_obs_his.pregnancy[int(index)-1].antenatal.nature_of_labor)
            except:
                nat_of_lab_form = NatureOfLaborForm()
                antenatal_data = None
            try:
                post_nal_form = PostnatalForm(instance = case_obs_his.pregnancy[int(index)-1].postnatal)
            except:
                post_nal_form = PostnatalForm()
            try:
                child_form = ChildForm(instance = case_obs_his.pregnancy[int(request.GET.get('pregnancy_index_no'))-1].child[(int(request.GET.get('child_index_no'))-1)])
            except:
                child_form = ChildForm()
        else:
            child_form = ChildForm()
            post_nal_form = PostnatalForm()
            nat_of_lab_form = NatureOfLaborForm()
        
        return render(request,'case_history/obstreric_history.html',{
                                                                    'nat_of_lab_form':nat_of_lab_form ,
                                                                    'post_nal_form':post_nal_form ,
                                                                    'child_form':child_form ,
                                                                    'case_id':case_id ,
                                                                    'success_note':success ,
                                                                    'case_obs_his':case_obs_his,
                                                                    'antenatal_data':antenatal_data,
                                                                    'pre_preg_index_no':request.GET.get('pre_preg_index_no'),
                                                                    'pregnancy_index_no':pregnancy_index_no,
                                                                    'antenatal_index_no':request.GET.get('antenatal_index_no'),
                                                                    'postnatal_index_no':request.GET.get('postnatal_index_no'),
                                                                    'child_index_no':request.GET.get('child_index_no'),
                                                                    'gravida_data':gravida_data,
                                                                    'para_data':para_data,
                                                                    'abortion_data':abortion_data,
                                                                    'stillbirth_data':stillbirth_data,
                                                                    'living_data':living_data,
                                                                    'obs_his_save':obs_his_save,
                                                                    'save_index_no':save_index_no,
                                                                })
        
    elif request.method == 'POST':
        if case_id :
            if CaseObstetricHistory.objects.filter(case_id = case_id).exists():
                case_obs_his = CaseObstetricHistory.objects.get(case_id = case_id)
            else:
                case_obs_his = CaseObstetricHistory(case_id = case_id,
                            previous_pregnancies = None,
                            pregnancy = None
                        )
                case_obs_his.save()
                
            comp_during_pregnancy_list = []
            comp_during_pregnancy_id = list(map(str,request.POST.getlist('comp_during_pregnancy')))
            for i in comp_during_pregnancy_id:
                comp_during_list = [ComplaintsDuringPregnancy(comp_during_pregnancy = DiseaseMaster.objects.get(id=i),
                                    remarks = request.POST.get('complaint_during_pregnancy_remarks'))
                                ]
                comp_during_pregnancy_list.extend(comp_during_list)
            
            if request.POST.get('field_name') or request.POST.get('index_no'):
                field_name = request.POST.get('field_name')
                if request.POST.get('field_name') == 'Previous Pregnancy':
                    case_obs_his.previous_pregnancies = None
                elif request.POST.get('field_name') == 'Postnatal':
                    case_obs_his.pregnancy[int(request.POST.get('preg_delete_index_no'))-1].postnatal = Postnatal()
                elif request.POST.get('field_name') == 'Antenatal':
                    case_obs_his.pregnancy[int(request.POST.get('preg_delete_index_no'))-1].antenatal = Antenatal(
                                                                                                period_of_pregnancy = None,
                                                                                                complaints_during_pregnancy = None,
                                                                                                nature_of_labor = NatureOfLabor(),
                                                                                                nature_of_delivery = None
                                                                                            )
                elif request.POST.get('field_name') == 'Child':
                    case_obs_his.pregnancy[int(request.POST.get('preg_delete_index_no'))-1].child.pop(int(request.POST.get('index_no'))-1)
                
                request.session['success_msg'] = field_name +_(" details has been deleted successfully.")
                case_obs_his.save()
            
            elif ("obs_form" in request.POST or request.POST.get('pre_preg_index_no')) and case_id:
                case_obs_his.previous_pregnancies = [
                    ObstetricHistory(
                        prev_pregnancies = request.POST.get('gravida'),
                        value = request.POST.get('gravida_value'),
                        ),
                        ObstetricHistory(
                        prev_pregnancies = request.POST.get('para'),
                        value = request.POST.get('para_value'),
                        ),
                        ObstetricHistory(
                        prev_pregnancies = request.POST.get('abortion'),
                        value = request.POST.get('abortion_value'),
                        ),
                        ObstetricHistory(
                        prev_pregnancies = request.POST.get('stillbirth'),
                        value = request.POST.get('stillbirth_value'),
                        ),
                        ObstetricHistory(
                        prev_pregnancies = request.POST.get('living'),
                        value = request.POST.get('living_value'),
                        )
                    ]
                case_obs_his.save()
                request.session['success_msg'] = _("Previous Pregnancy details has been saved successfully.")
            
            elif int(request.POST.get('new_add_pregnancy_index_no')) <= 1  and case_id:
                if int(request.POST.get('new_add_pregnancy_index_no')) == 1 and not case_obs_his.pregnancy:
                    case_obs_his.pregnancy = [Pregnancy(
                            antenatal = Antenatal(
                                period_of_pregnancy = None,
                                complaints_during_pregnancy = None,
                                nature_of_labor = NatureOfLabor(),
                                nature_of_delivery = None),
                            postnatal = Postnatal(),
                            child = None)]
                if 'antenatal_form' in request.POST and case_id:
                    nat_of_lab_form = NatureOfLaborForm(request.POST)
                    if nat_of_lab_form.is_valid():
                        nat_of_lab_data = {k: v for k, v in nat_of_lab_form.cleaned_data.items()}
                        if request.POST.get('pregnancy_index_no') and case_obs_his:
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_labor = NatureOfLabor(**nat_of_lab_data)
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.period_of_pregnancy = request.POST.get('period_of_pregnancy') 
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_delivery = request.POST.get('nature_of_delivery')
                            if request.POST.get('nature_of_delivery') == 'Normal':
                                case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_delivery_normal = request.POST.get('nature_of_delivery_normal')
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.complaints_during_pregnancy = comp_during_pregnancy_list
    #                     else:
    #                         case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_labor = NatureOfLabor(**nat_of_lab_data)
    #                         case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.period_of_pregnancy = request.POST.get('period_of_pregnancy') 
    #                         case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_delivery = request.POST.get('nature_of_delivery') 
    #                         if request.POST.get('nature_of_delivery') == 'Normal':
    #                             case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.nature_of_delivery_normal = request.POST.get('nature_of_delivery_normal')
    #                         case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].antenatal.complaints_during_pregnancy = comp_during_pregnancy_list
                        case_obs_his.save()
                        request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                        request.session['obs_his_save'] = 'ObstetricHistorySave'
                        request.session['success_msg'] = _("Antenatal details has been saved successfully.")
                
                elif "post_nal_form" in request.POST and case_id:
                    post_nal_form = PostnatalForm(request.POST)
                    if post_nal_form.is_valid():
                        post_nal_data = {k: v for k, v in post_nal_form.cleaned_data.items()}
                        if request.POST.get('pregnancy_index_no') and case_obs_his:
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].postnatal = Postnatal(**post_nal_data)
    #                     else:
    #                         case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].postnatal = Postnatal(**post_nal_data)
                        case_obs_his.save()
                        request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                        request.session['obs_his_save'] = 'ObstetricHistorySave'
                        request.session['success_msg'] = _("Postnatal details has been saved successfully.")
    
                elif "child_form" in request.POST and case_id:
                    child_form = ChildForm(request.POST)
                    if child_form.is_valid():
                        child_data = {k: v for k, v in child_form.cleaned_data.items()}
                        if request.POST.get('pregnancy_index_no') and request.POST.get('child_index_no') and case_obs_his:
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].child.pop(int(request.POST.get('child_index_no'))-1)
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].child.insert(int(request.POST.get('child_index_no'))-1, Child(**child_data))
                        elif request.POST.get('pregnancy_index_no') and case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].child:
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].child.extend([Child(**child_data)])
                        else:
                            case_obs_his.pregnancy[int(request.POST.get('pregnancy_index_no'))-1].child = [Child(**child_data)]
                        case_obs_his.save()
                        request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                        request.session['obs_his_save'] = 'ObstetricHistorySave'
                        request.session['success_msg'] = _("Child details has been saved successfully.")
                
                
            elif int(request.POST.get('new_add_pregnancy_index_no'))  > 1 and not request.POST.get('field_name') and case_obs_his:
                case_obs_his.pregnancy.extend([Pregnancy(
                        antenatal = Antenatal(
                            period_of_pregnancy = None,
                            complaints_during_pregnancy = None,
                            nature_of_labor = NatureOfLabor(),
                            nature_of_delivery = None),
                        postnatal = Postnatal(),
                        child = None)])
                if 'antenatal_form' in request.POST and case_obs_his:
                    nat_of_lab_form = NatureOfLaborForm(request.POST)
                    if nat_of_lab_form.is_valid():
                        nat_of_lab_data = {k: v for k, v in nat_of_lab_form.cleaned_data.items()}
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].antenatal.nature_of_labor = NatureOfLabor(**nat_of_lab_data)
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].antenatal.period_of_pregnancy = request.POST.get('period_of_pregnancy') 
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].antenatal.nature_of_delivery = request.POST.get('nature_of_delivery')
                        if request.POST.get('nature_of_delivery') == 'Normal':
                            case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].antenatal.nature_of_delivery_normal = request.POST.get('nature_of_delivery_normal')
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].antenatal.complaints_during_pregnancy = comp_during_pregnancy_list
                    case_obs_his.save()
                    request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                    request.session['obs_his_save'] = 'ObstetricHistorySave'
                    request.session['success_msg'] = _("Antenatal details has been saved successfully.")

                elif "post_nal_form" in request.POST and case_obs_his:
                    post_nal_form = PostnatalForm(request.POST)
                    if post_nal_form.is_valid():
                        post_nal_data = {k: v for k, v in post_nal_form.cleaned_data.items()}
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].postnatal = Postnatal(**post_nal_data)
                    case_obs_his.save()
                    request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                    request.session['obs_his_save'] = 'ObstetricHistorySave'
                    request.session['success_msg'] = _("Postnatal details has been saved successfully.")
                
                elif "child_form" in request.POST and case_obs_his:
                    child_form = ChildForm(request.POST)
                    if child_form.is_valid():
                        child_data = {k: v for k, v in child_form.cleaned_data.items()}
                        case_obs_his.pregnancy[int(request.POST.get('new_add_pregnancy_index_no'))-1].child = ([Child(**child_data)])
                    case_obs_his.save()
                    request.session['save_index_no'] = request.POST.get('pregnancy_index_no')
                    request.session['obs_his_save'] = 'ObstetricHistorySave'
                    request.session['success_msg'] = _("Child details has been saved successfully.")
            
            return HttpResponseRedirect(reverse_lazy('case_history:obstreric_history', args=[case_id]))  
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:obstreric_history'))
"""Obstreric history functionality - End here"""


"""Repertorisation history functionality - starts here"""
@login_required
def repertorisation(request, case_id=None):
    if request.method == 'GET':
        success = request.session.pop('success_msg', None)
        try:
            repert_record = CaseRepertorisation.objects.get(case_id=case_id)
        except:
            repert_record =None
        if (request.GET.get('sym_repert_index_no') or request.GET.get('medicin_index_no')) and repert_record:
            try:
                sym_form = SymptomsRepertorizedForm(instance=repert_record.symptoms_repertorized[int(request.GET.get('sym_repert_index_no'))-1])
            except:
                sym_form = SymptomsRepertorizedForm()
            try:
                medi_form = MedicineForm(instance=repert_record.medicines[int(request.GET.get('medicin_index_no'))-1])
            except:
                medi_form = MedicineForm()
        else:
            sym_form = SymptomsRepertorizedForm()
            medi_form = MedicineForm()

        return render(request,'case_history/repertorisation.html',{ 
                                                                    'case_id':case_id,
                                                                    'sym_form':sym_form,
                                                                    'medi_form':medi_form,
                                                                    'success_note':success,
                                                                    'repert_record':repert_record,
                                                                    'sym_repert_index_no':request.GET.get('sym_repert_index_no'),
                                                                    'medicin_index_no':request.GET.get('medicin_index_no')
                                                                })
    elif request.method == 'POST':
        if case_id:
            if CaseRepertorisation.objects.filter(case_id=case_id).exists():
                case_repert_record = CaseRepertorisation.objects.get(case_id=case_id)
            else:
                case_repert_record = CaseRepertorisation(
                        case_id = case_id,
                        computerized_manual_report = None,
                        symptoms_repertorized = None,
                        medicines = None,
                    )
    #             case_repert_record.save()
            
            symtoms_rep = list(map(str,request.POST.getlist('symptoms_repertor')))
            symtoms_list = []
            for i in symtoms_rep:
                if not i.isalpha() and SymptomsMaster.objects.filter(_id=i).exists():
                    sym = SymptomsMaster.objects.get(_id=i)
                    symtoms_list.append(sym.sym_name)
                else:
                    symtoms_list.append(i)
    #       Delete Condition Starts
            if request.POST.get('delete_entity'):
                if request.POST.get('field_name') == 'computerized_manual_report':
                    case_repert_record.computerized_manual_report = None
                    case_repert_record.save()
                    request.session['success_msg'] = _("Computerized / Manual Report has been deleted successfully.")
                elif request.POST.get('field_name') == 'symptoms_repertorized':
                    case_repert_record.symptoms_repertorized.pop(int(request.POST.get('index_no'))-1)
                    case_repert_record.save()
                    request.session['success_msg'] = _("Symptoms Repertorized details has been deleted successfully.")
                elif request.POST.get('field_name') == 'medicines':
                    case_repert_record.medicines.pop(int(request.POST.get('index_no'))-1)
                    case_repert_record.save()
                    request.session['success_msg'] = _("Medicines details has been deleted successfully.")
    #       Delete Condition Starts
            elif "computerized_manual_report" in request.POST and case_id:
                report_data = request.FILES.get('report_upload', None)
                if report_data:
                    case_repert_record.computerized_manual_report = report_data
                    case_repert_record.save()
                    request.session['success_msg'] = _("Computerized / Manual Report has been saved successfully.")
            elif "symptoms_repertorized" in request.POST and case_id:
                if case_repert_record and request.POST.get('sym_repert_index_no'):
                    case_repert_record.symptoms_repertorized.pop(int(request.POST.get('sym_repert_index_no'))-1)
                    case_repert_record.symptoms_repertorized.insert(int(request.POST.get('sym_repert_index_no'))-1, SymptomsRepertorized(symptoms_repertor = (','.join(symtoms_list))))
                elif case_repert_record.symptoms_repertorized:
                    case_repert_record.symptoms_repertorized.extend([SymptomsRepertorized(symptoms_repertor = (','.join(symtoms_list)))])
                else:
                    case_repert_record.symptoms_repertorized = [SymptomsRepertorized(symptoms_repertor = (','.join(symtoms_list)))]
                case_repert_record.save()
                request.session['success_msg'] = _("Symptoms Repertorized details has been saved successfully.")
            elif "medicines" in request.POST and case_id:
                medi_form = MedicineForm(request.POST)
                if medi_form.is_valid():
                    medi_data = {k: v for k, v in medi_form.cleaned_data.items()}
                    if case_repert_record and request.POST.get('medicin_index_no'):
                        case_repert_record.medicines.pop(int(request.POST.get('medicin_index_no'))-1)
                        case_repert_record.medicines.insert(int(request.POST.get('medicin_index_no'))-1, Medicine(**medi_data))
                    elif case_repert_record.medicines:
                        case_repert_record.medicines.extend([Medicine(**medi_data)])
                    else:
                        case_repert_record.medicines = [Medicine(**medi_data)]
                    case_repert_record.save()
                    request.session['success_msg'] = _("Medicine details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:repertorisation', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:repertorisation'))  

"""Repertorisation history functionality - ends here"""

"""Miasamatic analysis functionality - starts here"""
@login_required
def miasamatic_analysis(request, case_id=None):
    if request.method == 'GET':
        miasm_hist = pso_miasm = syco_miasm = syp_miasm = tub_miasm = None
        success = request.session.pop('success_msg',None)
        try:
            miasm_hist = CaseMiasamaticAnalysis.objects.get(case_id=case_id)
            pso_miasm = miasm_hist.predominant_miasm[0]
            syco_miasm = miasm_hist.predominant_miasm[1]
            syp_miasm = miasm_hist.predominant_miasm[2]
            tub_miasm = miasm_hist.predominant_miasm[3]
        except:
            miasm_hist = None
            pso_miasm = None
            syco_miasm = None
            syp_miasm = None
            tub_miasm = None
        return render(request,'case_history/miasamatic_analysis.html',{'case_id':case_id,
                                                                   'success_note':success,
                                                                   'miasm_hist':miasm_hist,
                                                                   'pso_miasm':pso_miasm,
                                                                   'syco_miasm':syco_miasm,
                                                                   'syp_miasm':syp_miasm,
                                                                   'tub_miasm':tub_miasm  
                                                                })
    if request.method == 'POST':
        if case_id:
            if CaseMiasamaticAnalysis.objects.filter(case_id=case_id).exists():
                miasm_obj = CaseMiasamaticAnalysis.objects.get(case_id=case_id)
            else:
                miasm_obj = CaseMiasamaticAnalysis(case_id=case_id,
                                                   predominant_miasm = None
                                                )
            if request.POST.get('case_record_miasm'):
                miasm_obj.predominant_miasm = [PredominantMiasm(
                                predominant_miasm = request.POST.get('psora'),
                                remarks = request.POST.get('psora_remarks'),
                                    ),
                                PredominantMiasm(
                                predominant_miasm = request.POST.get('sycosis'),
                                remarks = request.POST.get('sycosis_remarks'),
                                    ),
                                PredominantMiasm(
                                predominant_miasm = request.POST.get('syphillis'),
                                remarks = request.POST.get('syphillis_remarks'),
                                    ),
                                PredominantMiasm(
                                predominant_miasm = request.POST.get('tubercular'),
                                remarks = request.POST.get('tubercular_remarks'),
                                    )]
                miasm_obj.save()
                request.session['success_msg'] = _("Miasmatic Analysis has been updated successfully.")
                
            elif request.POST.get('delete_miasm_history'):
                miasm_obj.predominant_miasm = None
                miasm_obj.save()
                request.session['success_msg'] = _("Miasmatic Analysis has been deleted successfully.")
                
            else:
                miasm_obj.predominant_miasm = [PredominantMiasm(
                                                        predominant_miasm = request.POST.get('psora'),
                                                        remarks = request.POST.get('psora_remarks'),
                                                    ),
                                                    PredominantMiasm(
                                                    predominant_miasm = request.POST.get('sycosis'),
                                                    remarks = request.POST.get('sycosis_remarks'),
                                                        ),
                                                    PredominantMiasm(
                                                    predominant_miasm = request.POST.get('syphillis'),
                                                    remarks = request.POST.get('syphillis_remarks'),
                                                        ),
                                                    PredominantMiasm(
                                                    predominant_miasm = request.POST.get('tubercular'),
                                                    remarks = request.POST.get('tubercular_remarks'),
                                                        )]
                miasm_obj.save()
                request.session['success_msg'] = _("Miasmatic Analysis has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:miasamatic_analysis', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:miasamatic_analysis'))
"""Miasamatic analysis functionality - ends here"""
"""Physical examination finding functionality - starts here"""
@login_required
def physical_examination_finding(request, case_id="None"):
    if request.method == 'GET':
        success_msg = request.session.pop('success_msg',None)
        phy_exami_find = request.session.pop('phy_exami_find',None)
        try:
            case_record = CasePhysicalExaminationFindings.objects.get(case_id=case_id)
        except:
            case_record = None
        if case_record:
            general_examination = GeneralExaminationForm(instance=case_record.general_examination)
            system_examination = SystemicExaminationForm(instance=case_record.systemic_examination)
        else:
            general_examination = GeneralExaminationForm()
            system_examination = SystemicExaminationForm()
        return render(request,'case_history/physical_examination_finding.html',{'general_examination':general_examination,
                                                                                'system_examination':system_examination,
                                                                                'case_id':case_id,
                                                                                'case_record':case_record,
                                                                                'general_exami':request.GET.get('general_examination'),
                                                                                'systemic_exami':request.GET.get('systemic_examination'),
                                                                                'success_note':success_msg,
                                                                                'phy_exami_find':phy_exami_find
                                                                                })
    elif request.method == 'POST':
        if case_id :
            if CasePhysicalExaminationFindings.objects.filter(case_id = case_id).exists():
                case_physical_exam = CasePhysicalExaminationFindings.objects.get(case_id = case_id)
            else:
                case_physical_exam = CasePhysicalExaminationFindings(
                    case_id = case_id,
                    general_examination = GeneralExamination(),
                    systemic_examination = SystemicExamination()
                    )
                case_physical_exam.save()
            if request.POST.get('delete_present_complaint'):
                if request.POST.get('field_name') == "systemic_exam":
                     case_physical_exam.systemic_examination=SystemicExamination()
                     case_physical_exam.save()
                     request.session['success_msg'] = _("Systemic Examination has been deleted successfully.")
                if request.POST.get('field_name') == "general_examin":
                     case_physical_exam.general_examination=GeneralExamination()
                     case_physical_exam.save()
                     request.session['success_msg'] = _("General Examination has been deleted successfully.")
                
            elif case_id:
                case_physical_exam.general_examination = GeneralExamination(blood_pressure=request.POST.get('blood_pressure') if request.POST.get('blood_pressure') else case_physical_exam.general_examination.blood_pressure,
                                                                             pulse=request.POST.get('pulse') if request.POST.get('pulse') else case_physical_exam.general_examination.pulse,
                                                                            respiratory_rate=request.POST.get('respiratory_rate') if request.POST.get('respiratory_rate') else case_physical_exam.general_examination.respiratory_rate,
                                                                            cyanosis=request.POST.get('cyanosis') if request.POST.get('cyanosis') else case_physical_exam.general_examination.cyanosis,
                                                                            cyanosis_remarks=request.POST.get('cyanosis_remarks') if request.POST.get('cyanosis_remarks') else case_physical_exam.general_examination.cyanosis_remarks,
                                                                            jaundice=request.POST.get('jaundice') if request.POST.get('jaundice') else case_physical_exam.general_examination.jaundice,
                                                                            jaundice_remarks=request.POST.get('jaundice_remarks') if request.POST.get('jaundice_remarks') else case_physical_exam.general_examination.jaundice_remarks,
                                                                            anaemia=request.POST.get('anaemia') if request.POST.get('anaemia') else case_physical_exam.general_examination.anaemia, 
                                                                            anaemia_remarks=request.POST.get('anaemia_remarks') if request.POST.get('anaemia_remarks') else case_physical_exam.general_examination.anaemia_remarks,
                                                                            oedema=request.POST.get('oedema') if request.POST.get('oedema') else case_physical_exam.general_examination.oedema,
                                                                            oedema_remarks=request.POST.get('oedema_remarks') if request.POST.get('oedema_remarks') else case_physical_exam.general_examination.oedema_remarks, 
                                                                            lymphadenopathy=request.POST.get('lymphadenopathy') if request.POST.get('lymphadenopathy') else case_physical_exam.general_examination.lymphadenopathy,
                                                                            lymphadenopathy_remarks=request.POST.get('lymphadenopathy_remarks') if request.POST.get('lymphadenopathy_remarks') else case_physical_exam.general_examination.lymphadenopathy_remarks,
                                                                            clubbing=request.POST.get('clubbing') if request.POST.get('clubbing') else case_physical_exam.general_examination.clubbing, 
                                                                            clubbing_remarks=request.POST.get('clubbing_remarks') if request.POST.get('clubbing_remarks') else case_physical_exam.general_examination.clubbing_remarks )
                 
                case_physical_exam.systemic_examination = SystemicExamination(respiratory_system=request.POST.get('respiratory_system') if request.POST.get('respiratory_system') else case_physical_exam.systemic_examination.respiratory_system,
                                                                             cvs=request.POST.get('cvs') if request.POST.get('cvs') else case_physical_exam.systemic_examination.cvs,
                                                                            nervous_system=request.POST.get('nervous_system') if request.POST.get('nervous_system') else case_physical_exam.systemic_examination.nervous_system,
                                                                            gastro_intestinal_system=request.POST.get('gastro_intestinal_system') if request.POST.get('gastro_intestinal_system') else case_physical_exam.systemic_examination.gastro_intestinal_system,
                                                                            genito_urinary_system=request.POST.get('genito_urinary_system') if request.POST.get('genito_urinary_system') else case_physical_exam.systemic_examination.genito_urinary_system,
                                                                            locomotor_system=request.POST.get('locomotor_system') if request.POST.get('locomotor_system') else case_physical_exam.systemic_examination.locomotor_system,
                                                                            skin=request.POST.get('skin') if request.POST.get('skin') else case_physical_exam.systemic_examination.skin,
                                                                            others=request.POST.get('others') if request.POST.get('others') else case_physical_exam.systemic_examination.others)
                case_physical_exam.save()
                request.session['phy_exami_find'] = 'physical_examination_finding'
                request.session['success_msg'] = _("Physical Examination Findings details has been saved successfully.")
            return HttpResponseRedirect(reverse_lazy('case_history:physical_examination_finding', args=[case_id]))
        else:
            request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
            return HttpResponseRedirect(reverse_lazy('case_history:physical_examination_finding'))
        

"""Physical examination finding functionality - ends here"""
# 
# """Investigations categories functionality - starts here"""
# @login_required
# def investigations_categories(request, case_id=None):
#     if request.method == 'GET':
#         success = request.session.pop('success_msg',None)
#         
#         invast_mast = InvestigationsMaster.objects.all().values_list('id','investg_name')
#         case_record = CaseInvestigation.objects.filter(case_id=case_id)
#         invest_category = InvestigationCategoryMaster.objects.filter(status__status_name='Active')
#         map_case = InvestigationcategoryMapping.objects.filter(investg__case_id=case_id)
#         form10 = MiasamaticAnalysisForm()
#         return render(request,'case_history/investigations_categories.html',{'form10':form10,
#                                                                              'case_id':case_id,
#                                                                              'invest_category':invest_category,
#                                                                              'invast_mast':invast_mast,
#                                                                              'case_record':case_record,
#                                                                              'map_case':map_case,
#                                                                              'add_investigation':'add_investigation',
#                                                                              'success_msg':success,
#                                                                              'activeTab':request.GET.get('activeTab')})
# 
#     elif request.method == 'POST':
#         postdata_keys = [re.split('_+',key) for key in request.POST.keys() if re.match(r'^investigationname_\d+', key)]
#         if postdata_keys:
#             for each in postdata_keys:
#                 if  request.POST.get("investigationname_%s_%s" %(each[1],each[2]), None):
#                     investigation_value = request.POST.get("investigationname_%s_%s" %(each[1],each[2]), None)
#                 else:
#                     investigation_value = None
#                 if  request.POST.get("invstgationmaster_%s_%s" %(each[1],each[2]), None):
#                     investigation_master = request.POST.get("invstgationmaster_%s_%s" %(each[1],each[2]), None)
#                 else:
#                     investigation_master = None
#                 if  request.POST.get("inveatigationcategorymapping_%s_%s" %(each[1],each[2]), None):
#                     inveatigation_category_mapping = request.POST.get("inveatigationcategorymapping_%s_%s" %(each[1],each[2]), None)
#                 else:
#                     inveatigation_category_mapping = None
#                 if request.POST.get("case_investigation_%s_%s" %(each[1],each[2]), None):
#                     case_investigation = request.POST.get("case_investigation_%s_%s" %(each[1],each[2]), None)
#                 else:
#                     case_investigation = None
#                 if request.POST.get("case_investigation_categorymapping_%s_%s" %(each[1],each[2]), None):
#                     case_investigation_mapping = request.POST.get("case_investigation_categorymapping_%s_%s" %(each[1],each[2]), None)
#                 else:
#                     case_investigation_mapping = None
#                 if CaseInvestigation.objects.filter(case_id=case_id,id=case_investigation):
#                     if investigation_master:
#                         case_investiation = CaseInvestigation.objects.filter(case_id=case_id,id=case_investigation).update(
#                                                                         investg_mas_id=investigation_master)
#                 else : 
#                     if investigation_master:
#                         case_investiation = CaseInvestigation.objects.create(case_id=case_id,
#                                                                         investg_mas_id=investigation_master)
#                 if InvestigationcategoryMapping.objects.filter(id=case_investigation_mapping):
#                     investigation_category_map = InvestigationcategoryMapping.objects.filter(id=case_investigation_mapping).update(
#                                                                         investg_cat_id=inveatigation_category_mapping,
#                                                                         investg_cat_value=investigation_value)
#                 else:
#                     investigation_category_map = InvestigationcategoryMapping.objects.create(investg_id=case_investiation.id,
#                                                                         investg_cat_id=inveatigation_category_mapping,
#                                                                         investg_cat_value=investigation_value)
#             #Save the case status history starts
#             keep_case_status_history(case_id)
#             request.session['success_msg'] = _("Investigations Categories has been saved successfully.")
#         return HttpResponseRedirect(reverse_lazy('case_history:investigations_categories', args=[case_id]))
# """Investigations categories functionality - ends here"""
# 
# 
# """Medical management functionality - starts here"""
# @login_required
# def medical_management(request, case_id=None):
#     if request.method == 'GET':
#         success = request.session.pop('success_msg',None)
#         try:
#             case_record = CaseMedicineManagement.objects.get(case_id=case_id, prescription_order=1)
#             medi_pre_map = MedicinePrescriptionMapping.objects.get(medi_mgnt_id=case_record)
#         except:
#             case_record = None
#             medi_pre_map = None
#         if case_record:
#             med_form = MedicalManagementForm(instance=case_record)
#         else:
#             med_form = MedicalManagementForm()
#         prescription = MedicineMaster.objects.filter(status__status_name='Active').values_list('med_name','id')
#         return render(request,'case_history/medical_management.html',{'med_form':med_form,
#                                                                       'case_id':case_id,
#                                                                       'medi_pre_map':medi_pre_map,
#                                                                       'case_record':case_record,
#                                                                       'add_medical_managemant':'add_medical_managemant',
#                                                                       'activeTab':request.GET.get('activeTab'),
#                                                                       'success_msg':success,
#                                                                       'prescription':prescription
#                                                                     })
#     elif request.method == 'POST':
#         form = MedicalManagementForm(request.POST)
#         if form.is_valid():
#             data = {k: v for k, v in form.cleaned_data.items()}
#             if request.POST.get('medicine_managmentid'):
#                 medi_manag = CaseMedicineManagement.objects.filter(case_id=case_id,id=request.POST.get('medicine_managmentid')).update(
#                                                                prescription_order=request.POST.get('prescription_order'),
#                                                                **data)
#                 MedicinePrescriptionMapping.objects.filter(id=request.POST.get('medi_pres_map'), medi_mgnt_id = request.POST.get('medicine_managmentid')).update(
#                                                             prescription_id = request.POST.get('medicine_name'),
#                                                             potency=request.POST.get('potency'),
#                                                             dosage = request.POST.get('dosage'))
#             else:
#                 medi_manag = CaseMedicineManagement.objects.create(case_id=case_id,
#                                                                    prescription_order=request.POST.get('prescription_order'),
#                                                                    **data)
#                 MedicinePrescriptionMapping.objects.create(medi_mgnt_id = medi_manag.id,
#                                                             prescription_id = request.POST.get('medicine_name'),
#                                                             potency=request.POST.get('potency'),
#                                                             dosage = request.POST.get('dosage'))
#             #Save the case status history starts
#             keep_case_status_history(case_id)
#             request.session['success_msg'] = _("Medical Management has been saved successfully.")
#         return HttpResponseRedirect(reverse_lazy('case_history:medical_management', args=[case_id]))
# """Medical management functionality - ends here"""
# 
# """Add on therapy functionality - starts here"""
# @login_required
# def add_on_therapies(request, case_id=None):
#     if request.method == 'GET':
#         success = request.session.pop('success_msg',None)
#         #For edit/update case
#         if case_id:
#             AddontherayFormSet = modelformset_factory(CaseAddonTherapy, form=AddontherayForm, extra=0)
#             formset = AddontherayFormSet(queryset=CaseAddonTherapy.objects.filter(case_id=case_id, addon_order=1))
#             #If no data for particular case id
#             if len(formset) == 0:
#                 AddontherayFormSet = formset_factory(AddontherayForm)
#                 formset = AddontherayFormSet()
#         #For add case
#         else:
#             AddontherayFormSet = formset_factory(AddontherayForm)
#             formset = AddontherayFormSet()
#         success_msg = request.session.pop('success_msg', None)
#         return render(request,'case_history/add_on_therapies.html',{'case_id':case_id,
#                                                                     'add_therapies':'add_therapies',
#                                                                     'formset':formset,
#                                                                     'success_msg':success_msg,
#                                                                     'success_msg':success,
#                                                                     'activeTab':request.GET.get('activeTab')})
#     elif request.method== 'POST':
#         AddontherayFormSet = modelformset_factory(CaseAddonTherapy, form=AddontherayForm)
#         formset = AddontherayFormSet(request.POST)
#         if formset.is_valid():
#             instances = formset.save(commit=False)
#             for instance in instances:
#                 instance.case_id = case_id
#                 instance.addon_order = request.POST.get('addon_order')
#                 instance.save()
#             
#             #Save the case status history starts
#             keep_case_status_history(case_id)
#             request.session['success_msg'] = _("Addon Therapy has been saved successfully.")   
#         return HttpResponseRedirect(reverse_lazy('case_history:add_on_therapies', args=[case_id]))
# """Add on therapy functionality - ends here"""
"""CCRH add case history functionality - ends here"""

"""Based on the auto complete showing an Disease Name Starts here"""
def get_disease_names(request):
    results=[]
    search_result= {}
    if request.GET.get('case_id'):
        if request.GET.get('past_disease') or request.GET.get('present_diseases'):
            family_list =  CaseFamilyHistory.objects.get(case_id=request.GET.get('case_id'))
            relation_details = family_list.family_history[int(request.GET.get('realtion_index_no'))-1]
            if request.GET.get('past_disease'):
                for med in relation_details.diseases:
                    type_list_dis = DiseaseMaster.objects.filter(id = med.disease_id)
                    for dis in type_list_dis:
                        user_json = {}
                        user_json['id'] = dis.id
                        user_json['value'] = dis.dis_name
                        user_json['icd_code'] = dis.dis_icd_code
                        results.append(user_json)
            if request.GET.get('present_diseases'):
                for med in relation_details.present_diseases:
                    type_list_dis = DiseaseMaster.objects.filter(id = med.present_disease_id)
                    for dis in type_list_dis:
                        user_json = {}
                        user_json['id'] = dis.id
                        user_json['value'] = dis.dis_name
                        user_json['icd_code'] = dis.dis_icd_code
                        results.append(user_json)
        elif request.GET.get('antenatal_index_no'):
            obstetric_list =  CaseObstetricHistory.objects.get(case_id=request.GET.get('case_id'))
            pragnancy_deatils = obstetric_list.pregnancy[int(request.GET.get('antenatal_index_no'))-1]
            if request.GET.get('antenatal'):
                for med in pragnancy_deatils.antenatal.complaints_during_pregnancy:
                    type_list_dis = DiseaseMaster.objects.filter(id = med.comp_during_pregnancy_id)
                    for dis in type_list_dis:
                        user_json = {}
                        user_json['id'] = dis.id
                        user_json['value'] = dis.dis_name
                        user_json['icd_code'] = dis.dis_icd_code
                        results.append(user_json)
            
            if request.GET.get('nol'):       
                type_list_dis = DiseaseMaster.objects.filter(id = pragnancy_deatils.antenatal.nature_of_labor.nature_of_labor_id)
                for dis in type_list_dis:
                    user_json = {}
                    user_json['id'] = dis.id
                    user_json['value'] = dis.dis_name
                    user_json['icd_code'] = dis.dis_icd_code
                    results.append(user_json)
            
            if request.GET.get('postnatal'):       
                type_list_dis = DiseaseMaster.objects.filter(id = pragnancy_deatils.postnatal.nature_of_puerperium_id)
                for dis in type_list_dis:
                    user_json = {}
                    user_json['id'] = dis.id
                    user_json['value'] = dis.dis_name
                    user_json['icd_code'] = dis.dis_icd_code
                    results.append(user_json)
            
            if request.GET.get('child_index_no'):
                type_list_dis = DiseaseMaster.objects.filter(id = pragnancy_deatils.child[int(request.GET.get('child_index_no'))-1].cause_of_death_id)
                for dis in type_list_dis:
                    user_json = {}
                    user_json['id'] = dis.id
                    user_json['value'] = dis.dis_name
                    user_json['icd_code'] = dis.dis_icd_code
                    results.append(user_json)
        else:    
            type_list =  CaseHistory.objects.get(_id=request.GET.get('case_id'))
            if request.GET.get('primary_dign'):
                if type_list:
                        type_list_dis = DiseaseMaster.objects.filter(id = type_list.diagnosis.primary_diagnosis_id)
                        for dis in type_list_dis:
                            user_json = {}
                            user_json['id'] = dis.id
                            user_json['value'] = dis.dis_name
                            user_json['icd_code'] = dis.dis_icd_code
                            results.append(user_json)
            if request.GET.get('other_diagn'):
                if type_list:
                    for med in type_list.diagnosis.other_diagnosis:
                        type_list_dis = DiseaseMaster.objects.filter(id = med.diagnosis_id)
                        for dis in type_list_dis:
                            user_json = {}
                            user_json['id'] = dis.id
                            user_json['value'] = dis.dis_name
                            user_json['icd_code'] = dis.dis_icd_code
                            results.append(user_json)
                
    elif request.GET.get('primary_diagnosis'):
        search_result['dis_name__icontains'] = request.GET.get('primary_diagnosis')
        type_list = DiseaseMaster.objects.filter(**search_result)
        if type_list:
            for dis in type_list:
                user_json = {}
                user_json['id'] = dis.id
                user_json['value'] = dis.dis_name
                user_json['icd_code'] = dis.dis_icd_code
                results.append(user_json)
    else:
        if request.GET.get('value'):
            search_result['dis_name__icontains'] = request.GET.get('value')
        if request.GET.get('term'):
            search_result['dis_name__icontains'] = request.GET.get('term')
        type_list = DiseaseMaster.objects.filter(**search_result)
        if type_list:
            for dis in type_list:
                user_json = {}
                user_json['id'] = dis.id
                user_json['value'] = dis.dis_name
                user_json['icd_code'] = dis.dis_icd_code
                results.append(user_json)
    return JsonResponse({ 'list':results })
"""Based on the auto complete showing an Disease Name Ends here"""

"""Fetching the symptoms details starts here"""
def get_symptoms_names(request):
    results=[]
    if request.method == "GET":
        if request.GET.get('value'):
            type_list = SymptomsMaster.objects.filter(sym_name__icontains = request.GET.get('value'))
            for fos in type_list:
                user_json = {}
                user_json['id'] = json.loads(json_util.dumps(fos._id))['$oid']
                user_json['value'] = fos.sym_name
                results.append(user_json)
        elif request.GET.get('term'):
            query = request.GET.get("term", "")
            type_list_2 = SymptomsMaster.objects.filter(sym_name__icontains=query)
            if type_list_2:
                for dis in type_list_2:
                    user_json = {}
                    user_json['idd'] = json.loads(json_util.dumps(dis._id))
                    user_json['id'] = user_json['idd']['$oid']
                    user_json['value'] = dis.sym_name
                    results.append(user_json)
        elif request.GET.get('repert'):
            type_list = CaseRepertorisation.objects.get(case_id=request.GET.get('case_id'))
            if type_list:
                reper_sym = (type_list.symptoms_repertorized[int(request.GET.get('repert'))-1]).symptoms_repertor.split(',')
                for med in reper_sym:
                    type_list_sym = SymptomsMaster.objects.filter(sym_name = med)
                    if type_list_sym:
                        for dis in type_list_sym:
                            user_json = {}
                            user_json['id'] = json.loads(json_util.dumps(dis._id))['$oid']
                            user_json['value'] = dis.sym_name
                            results.append(user_json)
                    else:
                        user_json = {}
                        user_json['id'] = med
                        user_json['value'] = med
                        results.append(user_json) 
        return JsonResponse({'list':results}) 
    
"""Based on the investigation fetch investigation category starts here"""
def get_investigation_category(request):
    results=[]
    if request.method == "GET":
        type_list = InvestigationCategoryMaster.objects.filter(investg_mas_id = request.GET.get('value'))
        for fos in type_list:
                     user_json = {}
                     user_json['id'] = fos.id
                     user_json['value'] = fos.investg_cat_name
                     results.append(user_json)
        return JsonResponse({'list':results
                             }) 


"""To fetch the symptoms name based on auto complete  --starts here"""
class SymptomsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SymptomsMaster.objects.all()
        
        if self.q:
            qs = qs.filter(sym_name__icontains=self.q)
        return qs
    
"""To fetch the symptoms name based on auto complete --ends here"""

"""To fetch the symptoms name based on auto complete  --starts here"""
class DiseaseAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = DiseaseMaster.objects.all()
        
        if self.q:
            qs = qs.filter(dis_name__icontains=self.q)
        return qs
    
"""To fetch the symptoms name based on auto complete --ends here"""

"""To fetch the Mental General Conditions name based on auto complete  --starts here"""
class MentalAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MentalGeneralMaster.objects.all()
        if self.q:
            qs = qs.filter(mental_general_val__icontains=self.q)
        return qs
"""To fetch the Mental General Conditions name based on auto complete --ends here"""

# """Based on the auto complete showing an Disease Name Starts here"""
# def get_medicine_names(request):
#     results=[]
#     if request.GET.get('value'):
#         type_list = MedicineMaster.objects.filter(med_name__icontains = request.GET.get('value'))
#         if type_list:
#             for med in type_list:
#                 user_json = {}
#                 user_json['id'] = med.id
#                 user_json['value'] = med.med_name
#                 results.append(user_json)
#     return JsonResponse({ 'list':results })
# """Based on the auto complete showing an Disease Name Ends here"""

# """Add follow-up visit functionality - starts here"""
# @login_required
# def follow_up_add(request, order_no=None):
#     if request.method== 'POST':
#         #if you want to delete follow-up data on click of delete button --Starts here
#         if request.POST.get("followup_case_id"):
#             CasePhysicalFindings.objects.filter(case_id=request.POST.get("followup_case_id"),phyfind_order=request.POST.get("followup_order_id")).delete()
#             CaseMedicineManagement.objects.filter(case_id=request.POST.get("followup_case_id"),prescription_order=request.POST.get("followup_order_id")).delete()
#             CaseAddonTherapy.objects.filter(case_id=request.POST.get("followup_case_id"),addon_order=request.POST.get("followup_order_id")).delete()
#             request.session['success_msg'] = _('Follow-up details deleted successfully.')
#             return HttpResponseRedirect(reverse_lazy('case_history:add_case', args=[request.POST.get("followup_case_id")]))
#         
#         #if you want to delete follow-up data on click of delete button --Ends here
#         
#         #Create follow-up data --Starts here
#         elif request.POST.get('new_follow_up_visit_order'):
#             """Save for physical examinations finding --starts here"""
#             postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^physicaexaminationtype_\d+', key)]
#             if postdata_keys:
#                 for each in postdata_keys:
#                     if  request.POST.get("physicaexaminationtype_%s" % each, None):
#                         physcial_examination_type = request.POST.get("physicaexaminationtype_%s" % each, None)
#                     else:
#                         physcial_examination_type = None
#                     if  request.POST.get("physicalvalue_%s" % each, None):
#                         physical_exmaination_value = request.POST.get("physicalvalue_%s" % each, None)
#                     else:
#                         physical_exmaination_value = None
#                     case_physcial_examination = CasePhysicalFindings.objects.create(case_id = request.POST.get('case_record'),
#                                                                                 phyfind_order = request.POST.get('new_follow_up_visit_order'),
#                                                                                 fin_mas_id = physcial_examination_type,
#                                                                                 phyfind_value = physical_exmaination_value)
#             """Save for physical examinations finding --ends here"""
# 
#             """Save for medical management --starts here"""
#             case_medi_manag = CaseMedicineManagement.objects.create(case_id = request.POST.get('case_record'),
#                                                                     prescription_date = request.POST.get('prescription_date'),
#                                                                     prescription_order = request.POST.get('new_follow_up_visit_order'),
#                                                                     prescription_oridl_scale = request.POST.get('prescription_oridl_scale'),
#                                                                     outcome_of_prev_presc = request.POST.get('outcome_of_prev_presc'),
#                                                                     marks_for_improvement = request.POST.get('marks_for_improvement'),
#                                                                 )
#             MedicinePrescriptionMapping.objects.create(medi_mgnt_id = case_medi_manag.id,
#                                                             prescription_id = 114,
#                                                             potency=request.POST.get('potency'),
#                                                             dosage = request.POST.get('dosage'))
#             """Save for medical management --ends here""" 
#             
#             """Save for add on therapy --starts here"""
#             data_list=data_as_list(request.POST)
#             for i in data_list:
#                 CaseAddonTherapy.objects.create(case_id = request.POST.get('case_record'),
#                                                     addon_order = request.POST.get('new_follow_up_visit_order'),
#                                                     addon_thrpy_mas_id = i[0],
#                                                     medicine_name = i[1],
#                                                     medicine_dosage = i[2],
#                                                     duration_other_therapy = i[3],
#                                                     duration_after_which_other_therapy = i[4],
#                                                 )
#             """Save for add on therapy --ends here"""
#             request.session['success_msg'] = _('Follow-up details saved successfully.')
#             return HttpResponseRedirect(reverse_lazy('case_history:add_case', args=[request.POST.get('case_record')]))
#         #Create follow-up data --Ends here
#         
#         #Update follow-up data --Starts here
#         else:
#             """Update for physical examinations finding --starts here"""
#             postdata_keys = [key.split('_')[1] for key in request.POST.keys() if re.match(r'^physicaexaminationtype_\d+', key)]
#             if postdata_keys:
#                 for each in postdata_keys:
#                     if  request.POST.get("physicaexaminationtype_%s" % each, None):
#                         physcial_examination_type = request.POST.get("physicaexaminationtype_%s" % each, None)
#                     else:
#                         physcial_examination_type = None
#                     if  request.POST.get("physicalvalue_%s" % each, None):
#                         physical_exmaination_value = request.POST.get("physicalvalue_%s" % each, None)
#                     else:
#                         physical_exmaination_value = None
#                     if request.POST.get("physical_finfing_id_%s" % each, None):
#                         case_physical_finding_id = request.POST.get("physical_finfing_id_%s" % each, None)
#                     else:
#                         case_physical_finding_id = None
#                     if CasePhysicalFindings.objects.filter(id=case_physical_finding_id, case_id=request.POST.get('case_record')):
#                         case_physcial_examination = CasePhysicalFindings.objects.filter(id=case_physical_finding_id, case_id = request.POST.get('case_record'),
#                                                                                 phyfind_order = order_no).update(
#                                                                                 fin_mas_id = physcial_examination_type,
#                                                                                 phyfind_value = physical_exmaination_value)            
#             """Update for physical examinations finding --ends here"""
#  
#             """Update for medical management --starts here"""
#             CaseMedicineManagement.objects.filter(id = request.POST.get('case_medi_management'), 
#                                                     case_id = request.POST.get('case_record'),
#                                                     prescription_order = order_no,).update(
#                                                     prescription_date = request.POST.get('prescription_date'),
#                                                     prescription_oridl_scale = request.POST.get('prescription_oridl_scale'),
#                                                     outcome_of_prev_presc = request.POST.get('outcome_of_prev_presc'),
#                                                     marks_for_improvement = request.POST.get('marks_for_improvement'),
#                                                 )
#             MedicinePrescriptionMapping.objects.filter(id = request.POST.get('medi_pres_management'), 
#                                                             medi_mgnt_id = request.POST.get('case_medi_management')).update(
#                                                             prescription_id = request.POST.get('medicine_name_medi_manag'),
#                                                             potency=request.POST.get('potency'),
#                                                             dosage = request.POST.get('dosage'),
#                                                         )
#             """Update for medical management --ends here""" 
#              
#             """Update for add on therapy --starts here"""
#             data_list=data_as_list(request.POST)
#             for i in data_list:
#                 if i[5]:
#                     CaseAddonTherapy.objects.filter(id=i[5], case_id = request.POST.get('case_record'),addon_order = order_no,).update(
#                                                                     addon_thrpy_mas_id = i[0],
#                                                                     medicine_name = i[1],
#                                                                     medicine_dosage = i[2],
#                                                                     duration_other_therapy = i[3],
#                                                                     duration_after_which_other_therapy = i[4],
#                                                                 )
#                 else:
#                     CaseAddonTherapy.objects.create(case_id = request.POST.get('case_record'),
#                                                     addon_order = order_no,
#                                                     addon_thrpy_mas_id = i[0],
#                                                     medicine_name = i[1],
#                                                     medicine_dosage = i[2],
#                                                     duration_other_therapy = i[3],
#                                                     duration_after_which_other_therapy = i[4],
#                                                 )
#             """Update for add on therapy --ends here"""
#             request.session['success_msg'] = _('Follow-up details updated successfully.')
#             return HttpResponseRedirect(reverse_lazy('case_history:add_case', args=[request.POST.get('case_record')]))
#         #Update follow-up data --Ends here
# 
# """Add follow-up visit functionality - ends here"""

# """Click on submit making casestatus submitted starts here"""
# def case_submitted_status(request, case_id=None):
#     if case_id:
#         case_record_id = CaseHistory.objects.filter(casecomplaints__case_id = case_id,
# #                                                    casediagnosis__case_id = case_id,
#                                                    casefamilyhistory__case_id = case_id,
#                                                    caseinvestigation__case_id = case_id,
#                                                    casemedicinemanagement__case_id = case_id,
#                                                    casementalgeneral__case_id = case_id,
#                                                    casemiasamaticanalysis__case_id = case_id,
#                                                    caseobstrericchildhistory__case_id = case_id,
#                                                    caseobstrerichistory__case_id = case_id,
#                                                    casepasthistorydisease__case_id = case_id,
#                                                    casepersonalhistory__case_id = case_id,
#                                                    casepersonalhistoryothers__case_id = case_id,
#                                                    casephysicalfindings__case_id = case_id,
#                                                    casephysicalgeneral__case_id = case_id,
#                                                    caserepertorisation__case_id = case_id,
#                                                    caseaddontherapy__case_id = case_id,
#                                                 )
#         if case_record_id:
#             request.session['success_msg'] = _("Please wait for admin approval.")
#             CaseHistory.objects.filter(id = case_id).update(case_status_id=2,
#                                                             case_listing_status_id=2
#                                                             )
#             #Save the case status history starts
#             keep_case_status_history(case_id,case_status="Submitted")
#             
#             return HttpResponseRedirect(reverse_lazy('case_history:add_case', args=[case_id]))
#         else:
#             request.session['success_msg'] = _("Kindly fill all the tabs field before submit.")
#             return HttpResponseRedirect(reverse_lazy('case_history:add_on_therapies', args=[case_id]))


"""To fetch the State name based on auto complete  --starts here"""
class StateAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = State.objects.all()
        if self.q:
            qs = qs.filter(state_name__icontains=self.q)
        return qs
    
"""To fetch the State name based on auto complete --ends here"""

"""To fetch the city name based on auto complete  --starts here"""
class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        
        qs = City.objects.all()
        if self.q:
            qs = qs.filter(city_name__icontains=self.q)
        return qs
    
"""To fetch the city name based on auto complete --ends here"""

"""To fetch the Institute name based on auto complete  --starts here"""
class InstituteAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = HospitalMaster.objects.all()
        
        if self.q:
            qs = qs.filter(hospital_name__icontains=self.q)
        return qs
    
"""To fetch the Institute name based on auto complete --ends here"""

"""Based on the auto complete showing an Disease & Symptoms Name Starts here"""
def get_keywords_names(request):
    dis_results=[]
    sym_results=[]
    results = []
    if request.GET.get('term'):
        query = request.GET.get("term", "")
        type_list_1 = DiseaseMaster.objects.filter(dis_name__icontains=query)
        if type_list_1:
            for dis in type_list_1:
                user_json = {}
                user_json['id'] = dis.id
                user_json['value'] = dis.dis_name
                user_json['icd_code'] = dis.dis_icd_code
                dis_results.append(user_json)
                
        type_list_2 = SymptomsMaster.objects.filter(sym_name__icontains=query)
        if type_list_2:
            for dis in type_list_2:
                user_json = {}
                user_json['idd'] = json.loads(json_util.dumps(dis._id))
                user_json['id'] = user_json['idd']['$oid']
                user_json['value'] = dis.sym_name
                sym_results.append(user_json)
        results =  dis_results + sym_results
        
    elif request.GET.get('case_id'):
        type_list =  CaseHistory.objects.get(_id=request.GET.get('case_id'))
        if type_list:
            for med in type_list.keywords.case_keywords_symptoms:
                type_list_sym = SymptomsMaster.objects.filter(sym_name = med.keywords_symptoms)
                for dis in type_list_sym:
                    user_json = {}
                    user_json['idd'] = json.loads(json_util.dumps(dis._id))
                    user_json['id'] = user_json['idd']['$oid']
                    user_json['value'] = dis.sym_name
                    results.append(user_json)
            for med in type_list.keywords.case_keywords_disease:
                type_list_dis = DiseaseMaster.objects.filter(dis_name = med.keywords_disease)
                for dis in type_list_dis:
                    user_json = {}
                    user_json['id'] = dis.id
                    user_json['icd_code'] = dis.dis_icd_code
                    user_json['value'] = dis.dis_name
                    results.append(user_json)
            if type_list.keywords.other_keywords:
                other_keywords = type_list.keywords.other_keywords.split(",")
                for i in other_keywords:
                    user_json = {}
                    user_json['id'] = i
                    user_json['value'] = i
                    results.append(user_json)
    return JsonResponse({ 'list':results })
"""Based on the auto complete showing an Disease & Symptoms Name Ends here"""

"""To fetch the Symptoms  based on auto complete  --starts here"""
class SymptomsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = SymptomsMaster.objects.all()
        if self.q:
            qs =  qs.filter(sym_name__icontains=self.q)
        return qs
    
"""To fetch the Symptoms name based on auto complete --ends here"""

"""To fetch the Medicine  based on auto complete  --starts here"""
class MedicineAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = MedicineMaster.objects.all()
        if self.q:
            qs =  qs.filter(med_name__icontains=self.q)
        return qs
    
"""To fetch the Medicine name based on auto complete --ends here"""


# '''Follow up Practitioners Funtionality Starts Here'''
#     
#     
# from case_history.models import (MedicineFollowUpPractForm, SymptomsFollowUpPractForm,
#                                  CaseFollowUpPract,FollowUpPract,PatientOutcome)
# 
# def follow_up_practitioners(request, case_id=None):
#     MedicineFormSet = formset_factory(MedicineFollowUpPractForm)
#     SymptomsFormSet = formset_factory(SymptomsFollowUpPractForm)
#     if request.method== 'GET':
#         case_id = '5f437e7983ec1c9dea62a380'
#         formset = MedicineFormSet()
#         symformset = SymptomsFormSet()
#         return render(request,'case_history/follow_up_practitioners.html',{'formset':formset,
#                                                                        'symformset':symformset})
#     
#     elif request.method== 'POST':
#         case_id = '5f437e7983ec1c9dea62a380'
#         if case_id:
#             if CaseFollowUpPract.objects.filter(case_id=case_id).exists():
#                 case_followup_pract = CaseFollowUpPract.objects.get(case_id=case_id)
#             else:
#                 case_followup_pract = CaseFollowUpPract(
#                         case_id = case_id,
#                         follow_up = None)
#         
#             formset = MedicineFormSet(request.POST)
#             symformset = SymptomsFormSet(request.POST)
#             if formset.is_valid():
#                 instances = formset.save(commit=False)
#                 for instance in instances:
#                     instance.case_id = case_id
#                     instance.addon_order = request.POST.get('addon_order')
#                     instance.save()
#                  
#                 request.session['success_msg'] = _("Case Follow Up Practitioner details has been saved successfully.")   
#             return HttpResponseRedirect(reverse_lazy('case_history:follow_up_practitioners', args=[case_id]))
#         else:
#             request.session['success_msg'] = _("Please complete the Case Summary Tab in order to proceed further.")
#             return HttpResponseRedirect(reverse_lazy('case_history:follow_up_practitioners'))
# 
# '''Follow up Practitioners Funtionality Ends Here'''




