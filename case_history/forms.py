from django.contrib.auth import authenticate
from django import forms
from django.utils.translation import ugettext_lazy as _
from debug_toolbar.panels.sql.tracking import state

from case_history.models import (CaseHistory, CaseComplaints, CasePersonalHistory, 
                                )

from master.models import (State,City, DiseaseMaster, HabitsMaster,
                           SymptomsMaster, MentalGeneralMaster, HospitalMaster)
from user_profile.models import PractDetails

from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist
from dal import autocomplete
from django.template.context_processors import request


class AddCaseDetailsForm(forms.ModelForm):
    def autogenerate_case_id():
        last_case_id = CaseHistory.objects.all().order_by('_id').last()
        if not last_case_id:
            return 'HCCR' + '00001'
        case_id = last_case_id.case_id
        case_id_int = int(case_id[4:9])
        new_case_id_int = case_id_int + 1
        new_case_id = 'HCCR' + str(new_case_id_int).zfill(5)
        return new_case_id
    case_id = forms.CharField(label=_("Case ID*"), max_length=250, initial=autogenerate_case_id, widget=forms.HiddenInput(attrs={'class':'','readonly':'True', 'placeholder':_('')})) 
    case_title   =    forms.CharField(label=_("Title of the Case"), max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    case_summary   =  forms.CharField(label=_("Case Summary"), max_length=300, widget=forms.Textarea(attrs={'class':'form-control','rows':'5', 'cols':'50', 'placeholder':_('')})) 
    case_pract_id = forms.CharField(label=_("Homeopathic Practitioner ID"), max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'readonly':'True' ,'placeholder':_('')})) 
    name_of_institute_unit = forms.ChoiceField(label=_("Name of Institute /Unit /Affiliation"), widget=forms.Select(attrs={'class':'form-control'})) 

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        registration_no = PractDetails.objects.filter(user_id=user).values_list('pract_reg_no',flat=1)
        super(AddCaseDetailsForm, self).__init__(*args, **kwargs)
        try:
            self.fields['case_pract_id'].initial = registration_no[0]
        except:
            self.fields['case_pract_id'].initial = 'HCCR000'
        habit_diet_other_choices_dict = OrderedDict()
        for clinical in PractDetails.objects.filter(user_id=user).order_by("clinical_setting"):
            for habit in clinical.clinical_setting:
                choice_tuple = (habit.clinic_name, habit.clinic_name)
                try:
                    university_name = habit.get_hab_type_display()
                except (AttributeError, ObjectDoesNotExist):
                    university_name = False
                try:
                    habit_diet_other_choices_dict[university_name].append(choice_tuple)
                except KeyError:
                    habit_diet_other_choices_dict[university_name] = [choice_tuple]
        self.fields["name_of_institute_unit"].choices = habit_diet_other_choices_dict.items()

    class Meta:
        model = CaseHistory
        fields = ['case_title','case_summary','case_pract_id','name_of_institute_unit','case_id']
                   

class PatientDetailsForm(forms.ModelForm):
    Gender_CHOICES = (
        (u'', u'Select'),
        (u'Male', u'Male'),
        (u'Female', u'Female'),
        (u'Others', u'Others'),
        )
    MARITAL_CHOICES = (
        (u'', u'Select'),
        (u'Married', u'Married'),
        (u'UnMarried', u'UnMarried'),
        (u'Divorced', u'Divorced'),
        )
    case_patient_name   = forms.CharField(label=_("Name"), required=True, max_length=250, widget=forms.TextInput(attrs={'class':'form-control'}))      
    case_patient_father = forms.CharField(label=_("Father's Name"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control'}))      
    case_patient_mobile = forms.IntegerField(label=_("Mobile"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    case_patient_email = forms.EmailField(label=_("Email"), required=False, max_length=254, widget=forms.TextInput(attrs={'class':'email form-control', 'style':'text-transform:none;'}))
    case_patient_age   = forms.CharField(label=_("Age"), required=True, widget=forms.TextInput(attrs={'class':'form-control'})) 
    case_patient_sex   = forms.CharField(label=_("Gender"), required=True, max_length=10, widget=forms.Select(choices=Gender_CHOICES, attrs={'class':'form-control',})) 
    case_patient_address   = forms.CharField(label=_("Address"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    case_patient_occupation   = forms.CharField(label=_("Occupation"), max_length=250, required=False, widget=forms.TextInput(attrs={'class':'form-control',})) 
    case_patient_education = forms.CharField(label=_("Education"), max_length=250, required=False, widget=forms.TextInput(attrs={'class':'form-control', })) 
    case_patient_marital_status = forms.CharField(label=_("Marital status"), required=True, max_length=10, widget=forms.Select(choices=MARITAL_CHOICES, attrs={'class':'form-control', })) 
    case_patient_pin_code = forms.IntegerField(label=_("Pincode"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    case_patient_state = forms.ModelChoiceField(label=_("State"),
        queryset=State.objects.all(),
        widget=autocomplete.ModelSelect2(url='case_history:state-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    case_patient_city = forms.ModelChoiceField(label=_("City"),
        queryset=City.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:city-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    class Meta:
        model = CaseHistory
        fields = ['case_patient_name','case_patient_father','case_patient_mobile','case_patient_email','case_patient_city','case_patient_age','case_patient_sex','case_patient_address','case_patient_state',
                  'case_patient_occupation','case_patient_education','case_patient_marital_status','case_patient_pin_code']

class PresentComplaintForm(forms.ModelForm):
    Duration_CHOICES = (
        (u'1', u'Days'),
        (u'2', u'Month'),
        (u'3', u'Year'),
        (u'4', u'Weeks'),
    )

    comp_symptoms = forms.ModelChoiceField(label=_("Symptoms"),
        queryset=SymptomsMaster.objects.all(),
        widget=autocomplete.ModelSelect2(url='case_history:symptoms-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Type Symptoms Name', 'data-minimum-input-length': 2})
    )
    comp_duration = forms.CharField(label=_("Duration*"), max_length=250, widget=forms.TextInput(attrs={'class':'form-control valid_class_require number_valid', 'placeholder':_('Duration')})) 
    comp_duration_type   = forms.CharField(label=_("Duration Type"), required=True, max_length=1, widget=forms.Select(choices=Duration_CHOICES, attrs={'class':'form-control', 'placeholder':_('Duration Type')})) 
    comp_side = forms.CharField(label=_("Side*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25', 'placeholder':_('Side')})) 
    comp_time = forms.CharField(label=_("Time*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25', 'placeholder':_('Time')})) 
    comp_modality = forms.CharField(label=_("Modality*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25', 'placeholder':_('Modality')})) 
    comp_extension = forms.CharField(label=_("Extension*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25', 'placeholder':_('Extension')})) 
    comp_concomitants = forms.CharField(label=_("Concomitants*"), max_length=250, widget=forms.TextInput(attrs={'class':'form-control valid_class_require', 'placeholder':_('Concomitants')})) 

    class Meta:
        model = CaseComplaints
        fields = ['comp_symptoms','comp_duration','comp_duration_type','comp_side','comp_time','comp_modality',
                  'comp_extension','comp_concomitants',]
    
""""Personal History Model Form Starts Here"""
class PersonalHistoryForm(forms.ModelForm):
    Economy_Status_CHOICES= (
        (u'', u'Select'),
        (u'Lower', u'Lower'),
        (u'Middle', u'Middle'),
        (u'Higher', u'Higher'),
    )
    hobbies = forms.CharField(label=_("Hobbies"),required=False,  widget=forms.Textarea(attrs={'class':'form-control val_comma','rows':'3', 'cols':'4', 'placeholder':_('')})) 
    case_patient_economy_status   = forms.CharField(label=_("Economy Status"), max_length=100, widget=forms.Select(choices=Economy_Status_CHOICES, attrs={'class':'form-control', 'placeholder':_('')})) 

    class Meta:
        model = CasePersonalHistory
        fields = ['hobbies','case_patient_economy_status']
""""Personal History Model Form ENds Here"""


# class ObstetricHistoryForm(forms.ModelForm):
#     pbh_his_gravida = forms.CharField(label=_("Gravida*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Gravida')})) 
#     pbh_his_para = forms.CharField(label=_("Para*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Para')})) 
#     pbh_his_abortion = forms.CharField(label=_("Abortion*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Abortion')})) 
#     pbh_his_stillbirth = forms.CharField(label=_("Stillbirth*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Stillbirth')})) 
#     pbh_his_living = forms.CharField(label=_("Living*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Living')}))  
#     pbh_his_period_of_pregnancy = forms.CharField(label=_("Period Of Pregnancy*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Period Of Pregnancy')})) 
# #     pbh_his_lactation_history = forms.CharField(label=_("Lactation History"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Lactation History')}))
#     pbh_his_comp_dur_pregnancy = forms.CharField(label=_("Complaints During Pregnancy*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Complaints During Pregnancy')})) 
#     pbh_his_nature_of_labor = forms.CharField(label=_("Nature Of Labor*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Nature Of Labor')})) 
#     pbh_his_nature_of_delivery = forms.CharField(label=_("Nature Of Delivery*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Nature Of Delivery')})) 
#     pbh_his_nature_of_puerperium = forms.CharField(label=_("Nature Of Puerperium*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Nature Of Puerperium')})) 
# 
#     class Meta:
#         model = CaseObstrericHistory
#         fields = ['pbh_his_gravida','pbh_his_para','pbh_his_abortion','pbh_his_stillbirth','pbh_his_living',
#                   'pbh_his_period_of_pregnancy','pbh_his_comp_dur_pregnancy',
#                   'pbh_his_nature_of_labor','pbh_his_nature_of_delivery','pbh_his_nature_of_puerperium']
# 
#     
# class CaseObstrericChildHistoryForm(forms.ModelForm):
#     Child_Alive_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     chd_his_alive = forms.CharField(label=_("Alive"), max_length=1, widget=forms.Select(choices=Child_Alive_CHOICES, attrs={'class':'form-control'})) 
#     chd_his_causeofdeath = forms.CharField(label=_("Cause Of Death*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25'})) 
#     chd_his_birthweight = forms.CharField(label=_("Birth Weight*"), max_length=250, widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25'})) 
#     chd_his_child = forms.CharField(label=_("Lactation History*"), widget=forms.Textarea(attrs={'class':'form-control valid_class_require','rows':'3', 'cols':'25', 'placeholder':_('Lactation History')})) 
# 
#     class Meta:
#         model = CaseObstrericChildHistory
#         fields = ['chd_his_alive','chd_his_causeofdeath','chd_his_birthweight','chd_his_child']
#     

#     
# class MedicalManagementForm(forms.ModelForm):
#     prescription_date = forms.DateField(label=_("Date of Follow-up*"), widget=forms.TextInput(attrs={'class':'form-control date_picker', 'placeholder':_('Date of Follow-up')})) 
#     prescription_oridl_scale = forms.CharField(label=_("Prescription ORIDL Scale*"), widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Prescription ORIDL Scale')})) 
#     outcome_of_prev_presc = forms.CharField(label=_("Outcome of Previous prescription*"), widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Outcome of Previous prescription')})) 
#     marks_for_improvement = forms.CharField(label=_("Marks of Improvement*"), widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25', 'placeholder':_('Marks of Improvement')})) 
#     class Meta:
#         model = CaseMedicineManagement
#         fields = ['prescription_date','prescription_oridl_scale','outcome_of_prev_presc','marks_for_improvement']
#     
# class AddontherayForm(forms.ModelForm):
#     Duration_Temper_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     addon_thrpy_mas = forms.ModelChoiceField(queryset=AddonTherapyMaster.objects.all(), empty_label="Select Therapy", label=_("Thearpy*"), widget=forms.Select(attrs={'class':'form-control valid_class_require'}))
#     medicine_name = forms.CharField(label=_("Name of Medicines*"), max_length=100, widget=forms.TextInput(attrs={'class':'form-control valid_class_require', 'placeholder':_('Name of Medicines')})) 
#     medicine_dosage = forms.CharField(label=_("Dosage*"), max_length=100, widget=forms.TextInput(attrs={'class':'form-control valid_class_require', 'placeholder':_('Dosage')})) 
#     duration_other_therapy = forms.CharField(label=_("Duration of other therapy(Year/Months/Days)*"), max_length=100, widget=forms.TextInput(attrs={'class':'form-control valid_class_require', 'placeholder':_('Duration of other therapy(Year/Months/Days)')})) 
#     duration_after_which_other_therapy = forms.CharField(label=_("Duration after which other therapy (Allopathy/Ayurveda/ Siddha etc) was tapered after homoeopathic treatment*"), max_length=100, widget=forms.TextInput(attrs={'class':'form-control valid_class_require', 'placeholder':_("Duration after which other therapy (Allopathy/Ayurveda/ Siddha etc) was tapered after homoeopathic treatment")})) 
#     
#     class Meta:
#         model = CaseAddonTherapy
#         fields = ['addon_thrpy_mas','medicine_name','medicine_dosage','duration_other_therapy','duration_after_which_other_therapy']


