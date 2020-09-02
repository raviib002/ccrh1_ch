from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from audit_log.models.fields import CreatingUserField, LastUserField
from django.db.models.deletion import CASCADE
from random import choices
from dal import autocomplete
from master.models import (State, City, ClinicalSetting, DiseaseMaster,
                           CaseCategory,CaseCheckListMaster, SymptomsMaster,
                           MentalGeneralMaster, HabitsMaster, DietsMaster,
                           MedicineMaster
                           )
from user_profile.models import (PractDetails)
from django import forms
from collections import OrderedDict
from django.core.exceptions import ObjectDoesNotExist

'''Finalize case history models starts here'''    
#Case History History Model Starts Here
# Keywords using as Array Field in Case Personal History Starts Here
class KeywordsSymptoms(models.Model):
    keywords_symptoms = models.ForeignKey(SymptomsMaster,  on_delete=models.CASCADE, verbose_name=_("Case Keywords Symptoms"))

    def __str__(self):
        return self.keywords_symptoms.sym_name
    
    class Meta:
        abstract = True

class KeywordsDisease(models.Model):
    keywords_disease = models.ForeignKey(DiseaseMaster,  on_delete=models.CASCADE, verbose_name=_("Case Keywords Disease"))
    
    def __str__(self):
        return self.keywords_disease.dis_name
    
    class Meta:
        abstract = True

class Keywords(models.Model):
    case_keywords_symptoms = models.ArrayField(
        model_container=KeywordsSymptoms,
    )
    case_keywords_disease = models.ArrayField(
        model_container=KeywordsDisease,
    )
#     case_keywords_symptoms = models.CharField(max_length=250)
#     case_keywords_disease = models.CharField(max_length=250)
    other_keywords = models.TextField(verbose_name=_("Other Keywords"))

    def __str__(self):
        return self.other_keywords
    
    class Meta:
        abstract = True

class KeywordsForm(forms.ModelForm):
    class Meta:
            model = Keywords
            fields = (
                'case_keywords_symptoms','case_keywords_disease','other_keywords',
            )
#Keywords using as Array Field in Case Personal History Model Ends Here

# Diagnosis using as Array Field in Case Personal History Starts Here
class OtherDiagnosis(models.Model):
    diagnosis = models.ForeignKey(DiseaseMaster, on_delete=models.CASCADE, verbose_name=_("Other Diagnosis"))
    
    def __str__(self):
        return self.diagnosis.dis_name
    
    class Meta:
        abstract = True
        
class Diagnosis(models.Model):
    primary_diagnosis = models.ForeignKey(DiseaseMaster, on_delete=models.CASCADE, verbose_name=_("Primary Diagnosis"))
    other_diagnosis = models.ArrayField(
        model_container=OtherDiagnosis,
    )
#     primary_diagnosis = models.CharField(max_length=250)
#     other_diagnosis = models.CharField(max_length=250)

    def __str__(self):
        return self.primary_diagnosis.dis_name
    
    class Meta:
        abstract = True

class DiagnosisForm(forms.ModelForm):
    class Meta:
            model = Diagnosis
            fields = (
                'primary_diagnosis','other_diagnosis',
            )
# Diagnosis using as Array Field in Case Personal History Model Ends Here
class CaseHistory(models.Model):
    _id = models.ObjectIdField()
    case_id = models.CharField(max_length=250, unique=False, verbose_name=_("Case ID"))
    case_title = models.CharField(max_length=150, verbose_name=_("Case Title"))
    keywords = models.EmbeddedField(
        model_container=Keywords,
        model_form_class=KeywordsForm,
    )
    keyword_index = models.TextField(verbose_name=_("Keyword Index"))
    case_summary = models.TextField(verbose_name=_("Case Summary"))
    case_pract_id = models.CharField(max_length=150, verbose_name=_("Practitioner Registrations No"))
    name_of_institute_unit =  models.CharField(max_length=250, verbose_name=_("Name of Institute"))
    diagnosis = models.EmbeddedField(
        model_container=Diagnosis,
        model_form_class=DiagnosisForm,
    )
    case_status = models.CharField(max_length=150, verbose_name=_("Case Status"), help_text=_("Values will be stored as Submitted, Saved, Accepted, Under Review, Not Accepted, Processed, Reviewed, Published etc"))
    case_reviewer = models.ForeignKey(User, blank=True, null=True, related_name="CaseReviewer", on_delete=models.CASCADE, verbose_name=_("Case Reviewer"))
    case_supervisor =  models.ForeignKey(User, blank=True, null=True, related_name="CaseSupervisor",  on_delete=models.CASCADE, verbose_name=_("Case Supervisor"))
    case_category = models.CharField(max_length=150, verbose_name=_("Case Category"))

    def __str__(self):
        return self.case_title
    
    class Meta:
        verbose_name = "Case History"
        verbose_name_plural = "Case History"
        db_table = 'ccrh_case_history'
#         indexes = [
#             models.Index(fields=['case_id','keyword_index'])
#         ]
#Case History History Model Ends Here
    
#Case History Patient Detail Model Starts Here        
class CaseHistoryPatientDetail(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
    case_patient_name =  models.CharField(max_length=100, verbose_name=_("Patient Name"))
    case_patient_father = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Patient's Father Name"))
    case_patient_mobile  = models.BigIntegerField(blank=True, null=True, verbose_name=_("Patient Mobile Number ")) 
    case_patient_email = models.CharField(blank=True, null=True, max_length=100, verbose_name=_("Patient Email"))
    case_patient_age =  models.IntegerField(verbose_name=_("Patient Age"))
    case_patient_sex = models.CharField(max_length=100, verbose_name=_("Patient Sex"), help_text=_("Values will be stored as Male, Female, Others"))
    case_patient_address = models.TextField(blank=True, null=True, verbose_name=_("Patient Address"))
    case_patient_city = models.ForeignKey(City, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("City Name"))
    case_patient_state = models.ForeignKey(State, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("State Name"))
    case_patient_occupation = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Patient Occupation"))
    case_patient_marital_status = models.CharField(max_length=100, verbose_name=_("Marital Status"), help_text=_("Values will be stored as Married, Unmarried, Divorced"))
    case_patient_education = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Education"))
    case_patient_pin_code  = models.BigIntegerField(blank=True, null=True, verbose_name=_("Patient Pin Code ")) 
    
    def __str__(self):
        return self.case_patient_name
    
    class Meta:
        verbose_name = "Case History Patient Details"
        verbose_name_plural = "Case History Patient Details"
        db_table = 'ccrh_case_history_patient_detail'
        indexes = [
            models.Index(fields=['case_patient_name', 'case_patient_father','case_patient_sex','case_patient_city','case_patient_state'])
        ]
#Case History Patient Detail Model Ends Here

#Symptoms using as Array Field in Case Complaints Model Starts Here
class Symptoms(models.Model):   
    Duration_CHOICES = (
        (u'', u'Select'),
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    )
    comp_symptoms =  models.ForeignKey(SymptomsMaster,  on_delete=models.CASCADE, verbose_name=_("Case Symptoms"))
    comp_duration =  models.IntegerField(verbose_name=_("Complaint Duration"))
    comp_duration_type = models.CharField(max_length=10, choices=Duration_CHOICES, verbose_name=_("Complaints Duration Type"))
    comp_side = models.TextField(blank=True,null=True,  verbose_name=_("Complaints Side"))
    comp_time = models.TextField(blank=True,null=True,  verbose_name=_("Complaints Time"))
    comp_modality =  models.TextField(blank=True,null=True,  verbose_name=_("Complaints Modality"))
    comp_extension = models.TextField(blank=True,null=True,  verbose_name=_("Complaints Extension"))
    comp_concomitants = models.TextField(blank=True,null=True,  verbose_name=_("Complaints Concomitants"))
    
    
    def __str__(self):
        return self.comp_symptoms.sym_name
    
    class Meta:
        abstract = True


class SymptomsForm(forms.ModelForm):
    Duration_CHOICES = (
        (u'', u'Select'),
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    )
    comp_symptoms = forms.ModelChoiceField(label=_("Symptoms"),
        queryset=SymptomsMaster.objects.all(),
        widget=autocomplete.ModelSelect2(url='case_history:symptoms-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    comp_duration = forms.IntegerField(label=_("Duration"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    comp_duration_type   = forms.CharField(label=_("Duration Type"),required=False , max_length=10, widget=forms.Select(choices=Duration_CHOICES, attrs={'class':'duration_select'})) 
    comp_side = forms.CharField(label=_("Side"), max_length=250,required=False , widget=forms.TextInput(attrs={'class':'form-control'})) 
    comp_time = forms.CharField(label=_("Time"), max_length=250,required=False , widget=forms.TextInput(attrs={'class':'form-control'})) 
    comp_modality = forms.CharField(label=_("Modality"), required=False , max_length=250, widget=forms.TextInput(attrs={'class':'form-control'})) 
    comp_extension = forms.CharField(label=_("Extension"),required=False , max_length=250, widget=forms.TextInput(attrs={'class':'form-control'})) 
    comp_concomitants = forms.CharField(label=_("Concomitants"),required=False , max_length=250, widget=forms.TextInput(attrs={'class':'form-control'})) 
    
    class Meta:
        model = Symptoms
        fields = ['comp_symptoms','comp_duration','comp_duration_type','comp_side','comp_time','comp_modality',
                  'comp_extension','comp_concomitants',]
    
#Symptoms using as Array Field in Case Complaints Model Ends Here
class CaseComplaints(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, related_name="CaseComplaints", on_delete=models.CASCADE, verbose_name=_("Case History"))
    symptoms = models.ArrayField(
        model_container=Symptoms,
        model_form_class=SymptomsForm,
    )
    def __str__(self):
        return self.case.case_title
    
    class Meta:
        verbose_name = "Case Complaints"
        verbose_name_plural = "Case Complaints"
        db_table = 'ccrh_case_complaints'
#Case Complaints Model Ends Here

#Mental Generals using as Array Field in Case Mental General Model Starts Here
class MentalGenerals(models.Model):   
    ment_gen_id =   models.ForeignKey(MentalGeneralMaster, on_delete=models.CASCADE, verbose_name=_("Mental General Value "))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))

    def __str__(self):
        return self.ment_gen_id.mental_general_val
    
    class Meta:
        abstract = True

class MentalGeneralsForm(forms.ModelForm):
    ment_gen_id = forms.ModelChoiceField(label=_("Symptoms"),
        queryset=MentalGeneralMaster.objects.all(),
        widget=autocomplete.ModelSelect2(url='case_history:mental-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    remarks   = forms.CharField(label=_("Description"), required=False, max_length=300, widget=forms.Textarea(attrs={'class':'form-control'})) 
    class Meta:
        model = MentalGenerals
        fields = (
                'ment_gen_id','remarks',
            )
#Mental Generals using as Array Field in Case Mental General Model Ends Here
            
class CaseMentalGeneral(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    mental_generals = models.ArrayField(
        model_container=MentalGenerals,
        model_form_class=MentalGeneralsForm,
    )
    def __str__(self):
        return self.case.case_title
    
    class Meta:
        verbose_name = "Case Mental General"
        verbose_name_plural = "Case Mental General"
        db_table = 'ccrh_case_mental_general'
#Case Mental General Model Ends Here

#Case Personal History Model Starts Here
#Habits using as Array Field in Case Personal History Model Starts Here
class Habits(models.Model):   
    Hab_Duration_CHOICES= (
        (u'', u'Select'),
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    )
    habit = models.CharField(max_length=100, verbose_name=_("Habit"))
    habit_other =  models.CharField(max_length=250,blank=True,null=True, verbose_name=_("Other Habit"))
    hab_value = models.CharField(max_length=100, verbose_name=_("Habit Value"), help_text=_("Values will be stored as 1-Yes,2-No"))
    hab_duration =  models.IntegerField(blank=True, null=True, verbose_name=_("Habit Duration"))
    hab_duration_type = models.CharField(max_length=100, blank=True, null=True,choices=Hab_Duration_CHOICES, verbose_name=_("Habit Duration Type"))
    consumption_pattern =  models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Consumption Pattern"), help_text=_("Values will be stored as 1-Daily,2-Occasionally"))
    consumption_pattern_val =  models.CharField(max_length=100,blank=True,null=True, verbose_name=_("Consumption Pattern Value"))
    
    def __str__(self):
        return self.habit
    
    class Meta:
        abstract = True

class HabitsForm(forms.ModelForm):
    Habit_CHOICES= (
        (u'', u'Select Habit'),
        (u'Alcohosim', u'Alcohosim'),
        (u'Smoking', u'Smoking'),
        (u'Tobacco/Pan Chewing', u'Tobacco/Pan Chewing'),
        (u'Others', u'Others'),
    )
    Hab_Duration_CHOICES= (
        (u'', u'Select'),
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    )
    Hab_Pattern_CHOICES= (
        (u'', u'Select'),
        (u'Daily', u'Daily'),
        (u'Occasionaly', u'Occasionaly'),
        (u'Quantity', u'Quantity'),
    )
    
    habit = forms.ChoiceField(label=_("Habit"), widget=forms.Select(attrs={'class':'form-control'})) 
    habit_other = forms.CharField(label=_("Other Habit"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control duration_form', 'placeholder':_('')})) 
    hab_value = forms.CharField(label=_("Value"), required=False,initial=_('Yes'), max_length=100, widget=forms.HiddenInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    hab_duration = forms.IntegerField(label=_("Duration"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    hab_duration_type   = forms.CharField(label=_("Duration Type"), required=False, max_length=100, widget=forms.Select(choices=Hab_Duration_CHOICES, attrs={'class':'duration_select', 'placeholder':_('')})) 
    consumption_pattern = forms.CharField(label=_("Consumption Pattern"), required=False, max_length=100, widget=forms.Select(choices=Hab_Pattern_CHOICES, attrs={'class':'duration_select', 'placeholder':_('')})) 
    consumption_pattern_val = forms.CharField(label=_("Consumption Pattern"), required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control duration_form', 'placeholder':_('')})) 
    
    def __init__(self, *args, **kwargs):
        super(HabitsForm, self).__init__(*args, **kwargs)
        habit_choices_dict = OrderedDict()
        for habit in HabitsMaster.objects.all():
            choice_tuple = (habit.hab_name, habit.hab_name)
            try:
                habits_name = habit.get_hab_name_display()
            except (AttributeError, ObjectDoesNotExist):
                habits_name = False
            try:
                habit_choices_dict[habits_name].append(choice_tuple)
            except KeyError:
                habit_choices_dict[habits_name] = [choice_tuple]
        self.fields["habit"].choices = habit_choices_dict.items()

    class Meta:
            model = Habits
            fields = (
                'habit','habit_other','hab_value','hab_duration','hab_duration_type',
                'consumption_pattern','consumption_pattern_val',
            )
#Habits using as Array Field in Case Personal History Model Ends Here

#Diets using as Array Field in Case Personal History Starts Here
class Diets(models.Model):
    Diet_Duration_CHOICES= (
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    ) 
    diet = models.CharField(max_length=100, verbose_name=_("Diet"))
    diet_value = models.CharField(max_length=100, verbose_name=_("Diet Value"), help_text=_("Values will be stored as 1-Yes,2-No"))
    diet_duration =  models.IntegerField(blank=True, null=True, verbose_name=_("Diet Duration"))
    diet_duration_type = models.CharField(max_length=100, blank=True, null=True,choices=Diet_Duration_CHOICES, verbose_name=_("Diet Duration Type"))

    def __str__(self):
        return self.diet
    
    class Meta:
        abstract = True

class DietsForm(forms.ModelForm):
    Diet_CHOICES= (
        (u'', u'Select Habit'),
        (u'Veg', u'Veg'),
        (u'Non Veg', u'Non Veg'),
        (u'Eggetarian', u'Eggetarian'),
    )
    Diet_Duration_CHOICES= (
        (u'', u'Select'),
        (u'Days', u'Days'),
        (u'Month', u'Month'),
        (u'Year', u'Year'),
        (u'Weeks', u'Weeks'),
    )
    diet = forms.ChoiceField(label=_("Diet"), widget=forms.Select(attrs={'class':'form-control'})) 
    diet_value = forms.CharField(label=_("Value"), required=False,initial=_('Yes'), max_length=100, widget=forms.HiddenInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    diet_duration = forms.IntegerField(label=_("Duration"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    diet_duration_type   = forms.CharField(label=_("Duration Type"), required=False, max_length=100, widget=forms.Select(choices=Diet_Duration_CHOICES, attrs={'class':'duration_select', 'placeholder':_('')})) 

    def __init__(self, *args, **kwargs):
        super(DietsForm, self).__init__(*args, **kwargs)
        diet_choices_dict = OrderedDict()
        for diet in DietsMaster.objects.all():
            choice_tuple = (diet.diet_name, diet.diet_name)
            try:
                diets_name = diet.get_hab_name_display()
            except (AttributeError, ObjectDoesNotExist):
                diets_name = False
            try:
                diet_choices_dict[diets_name].append(choice_tuple)
            except KeyError:
                diet_choices_dict[diets_name] = [choice_tuple]
        self.fields["diet"].choices = diet_choices_dict.items()

    class Meta:
            model = Diets
            fields = (
                'diet','diet_value','diet_duration','diet_duration_type',
            )
#Diets using as Array Field in Case Personal History Model Ends Here

#Evolutionary History using as Array Field in Case Personal History Starts Here
class EvolutionaryHistory(models.Model):
    evl_history = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Evolutionary History"), help_text=_("Values will be stored as 1-Grief 2-Death of Loved One 3-Romantic Loss"))
    evl_history_others = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Evolutionary History Others"))

    def __str__(self):
        return self.evl_history
    
    class Meta:
        abstract = True

class EvolutionaryHistoryForm(forms.ModelForm):
    evl_history = forms.CharField(label=_("Evolutionary Development History Having Significant Impact On Health"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    evl_history_others = forms.CharField(label=_("Evolutionary History Others"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 

    class Meta:
            model = EvolutionaryHistory
            fields = (
                'evl_history','evl_history_others',
            )
#Evolutionary History using as Array Field in Case Personal History Model Ends Here

class CasePersonalHistory(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    habits = models.ArrayField(
        model_container=Habits,
        model_form_class=HabitsForm,
    )
    diets = models.ArrayField(
        model_container=Diets,
        model_form_class=DietsForm,
    )
    case_patient_economy_status = models.CharField(max_length=25, verbose_name=_("Economy Status"), help_text=_("Values will be stored as 1-Lower,2-Middle,3-Higher"))
    hobbies = models.TextField(blank=True, null=True, verbose_name=_("Hobbies"))
    evolutionary_history = models.EmbeddedField(
        model_container=EvolutionaryHistory,
        model_form_class=EvolutionaryHistoryForm,
        null=True
    )
   
    def __str__(self):
        return self.case.case_title
    
    class Meta:
        verbose_name = "Case Personal History"
        verbose_name_plural = "Case Personal History"
        db_table = 'ccrh_case_personal_history'
#Case Personal History Model Ends Here

#Case Family History Model Starts Here
#Family History using as Array Field in Case Past History Starts Here
class Diseases(models.Model):
    disease = models.ForeignKey(DiseaseMaster, on_delete=models.CASCADE, verbose_name=_("Disease"))
    dis_icd_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Disease ICD Code"))
    
    def __str__(self):
        return self.disease.dis_name
    
    class Meta:
        abstract = True
class DiseasesForm(forms.ModelForm):
    diseases = forms.ModelChoiceField(label=_("Past Disease"),
        queryset=DiseaseMaster.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2,'data-maximum-selection-length':10})
    )
    dis_icd_code = forms.CharField(label=_("Dis ICD Code"),required=False , max_length=250, widget=forms.TextInput(attrs={'class':'form-control'})) 

    class Meta:
            model = Diseases
            fields = (
                'disease','dis_icd_code',
            )
                    
class PresentDiseases(models.Model):
    present_disease = models.ForeignKey(DiseaseMaster, on_delete=models.CASCADE, verbose_name=_("Present Disease"))
    present_dis_icd_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Present Disease ICD Code"))
    
    def __str__(self):
        return self.present_disease.dis_name
    
    class Meta:
        abstract = True

class PresentDiseasesForm(forms.ModelForm):
    present_diseases = forms.ModelChoiceField(label=_("Present Disease"),
        queryset=DiseaseMaster.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2,'data-maximum-selection-length':10})
    )
    present_dis_icd_code = forms.CharField(label=_("Present Dis ICD code"),required=False , max_length=250, widget=forms.TextInput(attrs={'class':'form-control'})) 
    class Meta:
            model = PresentDiseases
            fields = (
                'present_disease','present_dis_icd_code',
            )
class FamilyHistory(models.Model):
    relation =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Relation"))
    alive_dead = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Alive Dead"), help_text=_("Values will be stored as Alive, Dead"))
    diseases = models.ArrayField(
        model_container = Diseases,
        model_form_class = DiseasesForm,
        null=True
    )
    present_diseases = models.ArrayField(
        model_container = PresentDiseases,
        model_form_class = PresentDiseasesForm,
        null=True
    )
    accidents = models.TextField(blank=True, null=True, verbose_name=_("Accidents"))

    def __str__(self):
        return self.relation
    
    class Meta:
        abstract = True

class FamilyHistoryForm(forms.ModelForm):
    class Meta:
            model = FamilyHistory
            fields = (
                'relation','alive_dead','diseases','present_diseases','accidents'
            )
#Family History using as Array Field in Case Past History Ends Here
class CaseFamilyHistory(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    family_history = models.ArrayField(
        model_container = FamilyHistory,
        model_form_class = FamilyHistoryForm,
    )
    
    def __str__(self):
        return self.case.case_title
    
    class Meta:
        verbose_name = "Case Family History"
        verbose_name_plural = "Case Family History"
        db_table = 'ccrh_case_family_his'
#Case Family History Model Ends Here

#Case Past History Model Starts Here
#Past History using as Array Field in Case Past History Starts Here
class PastHistory(models.Model):
    dis_name =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Disease Name"))
    year_of_onset =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Year of Onset"))
    age_of_onset = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Age of Onset"))
    treatment_histoy = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Treatment Histoy"))
    outcome =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Outcome"))
    reccurance = models.TextField(blank=True, null=True, verbose_name=_("Reccurance"))
    icd_code = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("ICD Code"))
    other_disease = models.TextField(blank=True, null=True, verbose_name=_("Other Diseases"))
    def __str__(self):
        return self.dis_name

    class Meta:
        abstract = True

class PastHistoryForm(forms.ModelForm):
    year_of_onset = forms.CharField(label=_("Year of Onset"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control type_of_suppression', 'placeholder':_('')})) 
    age_of_onset = forms.CharField(label=_("Age of Onset"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control year_of_suppression', 'placeholder':_('')})) 
    treatment_histoy = forms.CharField(label=_("Treatment History"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control age_of_suppression', 'placeholder':_('')})) 
    outcome = forms.CharField(label=_("Outcome"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control aetiology', 'placeholder':_('')})) 
    reccurance = forms.CharField(label=_("Reccurance"), required=False, widget=forms.TextInput(attrs={'class':'form-control other_information', 'placeholder':_('')})) 
    other_disease = forms.CharField(label=_("Others Disease"), required=False, widget=forms.TextInput(attrs={'class':'form-control other_disease', 'placeholder':_('')})) 

    class Meta:
            model = PastHistory
            fields = (
'dis_name','year_of_onset','age_of_onset','treatment_histoy','outcome','reccurance','icd_code','other_disease'
            )
#Past History using as Array Field in Case Past History Ends Here
#History Of Suppression using as Array Field in Case Past History Starts Here
class HistoryOfSuppression(models.Model):
    type_of_suppression = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Type of Suppression"))
    year_of_suppression =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Year of Suppression"))
    age_of_suppression = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Age of Suppression"))
    aetiology = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Reason of Suppression"))
    other_information = models.TextField(blank=True, null=True, verbose_name=_("Others Information"))

    def __str__(self):
        return self.year_of_suppression

    class Meta:
        abstract = True

class HistoryOfSuppressionForm(forms.ModelForm):
    type_of_suppression = forms.CharField(label=_("Type of Suppression"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control type_of_suppression', 'placeholder':_('')})) 
    year_of_suppression = forms.CharField(label=_("Year of Suppression"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control year_of_suppression', 'placeholder':_('')})) 
    age_of_suppression = forms.CharField(label=_("Age of Suppression"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control age_of_suppression', 'placeholder':_('')})) 
    aetiology = forms.CharField(label=_("Reason of Suppression"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control aetiology', 'placeholder':_('')})) 
    other_information = forms.CharField(label=_("Others Information"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control other_information', 'placeholder':_('')})) 
    
    class Meta:
            model = HistoryOfSuppression
            fields = (
                    'type_of_suppression','year_of_suppression','age_of_suppression','aetiology','other_information'
                    )
#History Of Suppression using as Array Field in Case Past History Ends Here
#Birth History using as Embedded Field in Case Past History Starts Here
class BirthHistory(models.Model):
    prematurity = models.TextField(blank=True, null=True, verbose_name=_("Prematurity"))
    birth_injuries = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Birth Injuries"))
    others_birth_injuries = models.TextField(blank=True, null=True, verbose_name=_("Other Birth Injuries"))
    birth_weight = models.TextField(blank=True, null=True, verbose_name=_("Birth Weight"))
    neonatal_complaints =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Neonatal Complaints"), help_text=_("Values will be stored as Neonatal Jaundice, Asphyxia Neonatorum, Congenital Defects"))
    others_neonatal_complaints = models.TextField(blank=True, null=True, verbose_name=_("Other Neonatal Complaints"))

    def __str__(self):
        return self.prematurity

    class Meta:
        abstract = True

class BirthHistoryForm(forms.ModelForm):
    Birth_Injuries_CHOICES= (
        (u'', u'Select'),
        (u'Forceps Delivery', u'Forceps Delivery'),
        (u'Delayed Labour', u'Delayed Labour'),
        (u'Cord Injury', u'Cord Injury'),
        (u'Others', u'Others'),
    )
    neonatal_complaints_CHOICES= (
        (u'', u'Select'),
        (u'Neonatal Jaundice', u'Neonatal Jaundice'),
        (u'Asphyxia Neonatorum', u'Asphyxia Neonatorum'),
        (u'Congenital Defects', u'Congenital Defects'),
    )
    prematurity = forms.CharField(label=_("Prematurity"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control prematurity', 'placeholder':_('')})) 
    birth_injuries = forms.CharField(label=_("Birth Injuries"), required=False, max_length=250, widget=forms.Select(choices=Birth_Injuries_CHOICES, attrs={'class':'form-control birth_injuries', 'placeholder':_('')})) 
    others_birth_injuries = forms.CharField(label=_("Others"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control others_birth_injuries_values', 'placeholder':_('')})) 
    birth_weight = forms.CharField(label=_("Birth Weight"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control birth_weight', 'placeholder':_('')})) 
    neonatal_complaints = forms.CharField(label=_("Neonatal Complaints"), required=False, max_length=250, widget=forms.Select(choices=neonatal_complaints_CHOICES, attrs={'class':'form-control neonatal_complaints', 'placeholder':_('')})) 
    others_neonatal_complaints = forms.CharField(label=_("Description"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control neonatal_complaints_val', 'placeholder':_('')})) 
    
    
    class Meta:
            model = BirthHistory
            fields = (
                'prematurity','birth_injuries','others_birth_injuries','birth_weight','neonatal_complaints','others_neonatal_complaints'
            )
#Birth History using as Embedded Field in Case Past History Ends Here
#Delivery His Details using as Embedded Field in Case Past History Starts Here
class DeliveryHisDetails(models.Model):
    delivery_history = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Delivery History"))
    premature_others = models.TextField(blank=True, null=True, verbose_name=_("Premature Others"))

    def __str__(self):
        return self.delivery_history

    class Meta:
        abstract = True

class DeliveryHisDetailsForm(forms.ModelForm):
    delivery_history_choices= (
        (u'', u'Select'),
        (u'Normal', u'Normal'),
        (u'Caesarean', u'Caesarean'),
        (u'Premature', u'Premature'),
    )
    premature_others = forms.CharField(label=_("Others"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control premature_others_values', 'placeholder':_('')})) 
    delivery_history = forms.CharField(label=_("Delivery"), required=False, max_length=250, widget=forms.Select(choices=delivery_history_choices, attrs={'class':'form-control mthr_helth_during_preg', 'placeholder':_('')})) 

    class Meta:
            model = DeliveryHisDetails
            fields = (
                'delivery_history','premature_others'
            )
#Delivery His Details using as Embedded Field in Case Past History Ends Here
#Mother Health History using as Embedded Field in Case Past History Starts Here
class MotherHealthHistory(models.Model):
    mthr_helth_during_preg = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Mother's Health During Pregnancy"))
    mthr_helth_during_preg_oth = models.TextField(blank=True, null=True, verbose_name=_("Mother's Health During Pregnancy Other"))

    def __str__(self):
        return self.mthr_helth_during_preg

    class Meta:
        abstract = True

class MotherHealthHistoryForm(forms.ModelForm):
    mthr_helth_during_preg_CHOICES= (
        (u'', u'Select'),
        (u'Toxemias', u'Toxemias'),
        (u'Fears', u'Fears'),
        (u'Stress', u'Stress'),
        (u'Trauma', u'Trauma'),
        (u'Radiation', u'Radiation'),
        (u'Vaccination', u'Vaccination'),
        (u'Family discord', u'Family discord'),
    )
    mthr_helth_during_preg_oth = forms.CharField(label=_("Others"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control mthr_helth_during_preg_oth', 'placeholder':_('')})) 
    mthr_helth_during_preg = forms.CharField(label=_("During Pregnancy"), required=False, max_length=250, widget=forms.Select(choices=mthr_helth_during_preg_CHOICES, attrs={'class':'form-control mthr_helth_during_preg', 'placeholder':_('')})) 

    class Meta:
            model = MotherHealthHistory
            fields = (
'mthr_helth_during_preg','mthr_helth_during_preg_oth'
            )
#Mother Health History using as Embedded Field in Case Past History Ends Here
#Breast Feeding History using as Embedded Field in Case Past History Starts Here
class BreastFeedingHistory(models.Model):
    duration = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Duration"))
    mothers_milk = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Mothers Milk"), help_text=_("Values will be stored as Craving, Aversion"))

    def __str__(self):
        return self.duration

    class Meta:
        abstract = True

class BreastFeedingHistoryForm(forms.ModelForm):
    breast_feeding_CHOICES= (
        (u'', u'Select'),
        (u'Craving', u'Craving'),
        (u'Aversion', u'Aversion'),
    )
    duration = forms.CharField(label=_("Duration"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control duration', 'placeholder':_('')})) 
    mothers_milk = forms.CharField(label=_("Mothers Milk"), required=False, max_length=250, widget=forms.Select(choices=breast_feeding_CHOICES, attrs={'class':'form-control mothers_milk', 'placeholder':_('')})) 
    class Meta:
            model = BreastFeedingHistory
            fields = (
                'duration','mothers_milk'
            )
#Breast Feeding History using as Embedded Field in Case Past History Ends Here

class HistoryOfChildren(models.Model):
    birth_history = models.EmbeddedField(
        model_container = BirthHistory,
        model_form_class = BirthHistoryForm,
        null=True
    )
    delivery_his_details = models.EmbeddedField(
        model_container = DeliveryHisDetails,
        model_form_class = DeliveryHisDetailsForm,
        null=True
    )
    mthr_helth_history = models.EmbeddedField(
        model_container = MotherHealthHistory,
        model_form_class = MotherHealthHistoryForm,
        null=True
    )
    breast_feeding_history = models.EmbeddedField(
        model_container = BreastFeedingHistory,
        model_form_class = BreastFeedingHistoryForm,
        null=True
    )
    def __str__(self):
        return self.birth_history

    class Meta:
        abstract = True

class HistoryOfChildrenForm(forms.ModelForm):
    class Meta:
            model = HistoryOfChildren
            fields = (
'birth_history','delivery_his_details','mthr_helth_history','breast_feeding_history'
            )


class CasePastHistory(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    past_history = models.ArrayField(
        model_container = PastHistory,
        model_form_class = PastHistoryForm,
    )
    history_of_suppression = models.ArrayField(
        model_container = HistoryOfSuppression,
        model_form_class = HistoryOfSuppressionForm,
    )
    injuries =  models.TextField(blank=True, null=True, verbose_name=_("Injuries"))
    accidents = models.TextField(blank=True, null=True, verbose_name=_("Accidents"))
    surgery = models.TextField(blank=True, null=True, verbose_name=_("Surgery"))
    history_of_children = models.EmbeddedField(
        model_container = HistoryOfChildren,
        model_form_class = HistoryOfChildrenForm,
        null=True
    )

    def __str__(self):
        return self.case.case_title

    class Meta:
        verbose_name = "Case Past History "
        verbose_name_plural = "Case Past History"
        db_table = 'ccrh_case_past_hist'
#Case Past History Model Ends Here

#Case Physical Examination Findings Model Starts Here
#General Examination using as Embedded Field in Case Physical Examination Findings Starts Here
class GeneralExamination(models.Model):
    blood_pressure = models.CharField(max_length=250,blank=True, null=True, verbose_name=_("Blood Pressure"), help_text=_("Values will be measured in 'mm of Hg'"))
    pulse = models.CharField(max_length=250, verbose_name=_("Pulse"), help_text=_("Values will be measured in 'per minute'"))
    respiratory_rate = models.CharField(max_length=250,blank=True, null=True, verbose_name=_("Respiratory Rate"), help_text=_("Values will be measured in 'per minute'"))
    cyanosis = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Cyanosis"))
    cyanosis_remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
    jaundice = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("jaundice"))
    jaundice_remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
    anaemia = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Anaemia"))
    anaemia_remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
    oedema = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Oedema"))
    oedema_remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
    lymphadenopathy = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Lymphadenopathy"))
    lymphadenopathy_remarks = models.TextField(blank=True, null=True, verbose_name=_("Lymphadenopathy Remarks"))
    clubbing = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Clubbing"))
    clubbing_remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))

    def __str__(self):
        return self.blood_pressure
   
    class Meta:
        abstract = True

class GeneralExaminationForm(forms.ModelForm):
    cyanosis_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
    Jaundice_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
    anaemia_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
    Oedema_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
    Lymphadenopathy_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
    Clubbing_choice = (
        (u'', u'Select'),
        (u'Yes', u'Yes'), 
        (u'No', u'No'),
    )
         
       
    blood_pressure = forms.CharField(label=_("Blood Pressure"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control blood_pressure', 'placeholder':_('')})) 
    pulse = forms.CharField(label=_("Pulse"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control pulse', 'placeholder':_('')})) 
    respiratory_rate = forms.CharField(label=_("Respiratory Rate "), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control respiratory_rate', 'placeholder':_('')})) 
    cyanosis = forms.CharField(required=False, label='Cyanosis', widget=forms.Select(choices=cyanosis_choice, attrs={'class':'form-control cyanosis'}))
    cyanosis_remarks = forms.CharField(label=_("Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control cyanosis_remarks_val', 'placeholder':_('')})) 
    jaundice = forms.CharField(required=False, label='Jaundice', widget=forms.Select(choices=Jaundice_choice, attrs={'class':'form-control jaundice'}))
    jaundice_remarks = forms.CharField(label=_("Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control jaundice_remarks_val', 'placeholder':_('')})) 
    anaemia = forms.CharField(required=False, label='Anaemia', widget=forms.Select(choices=anaemia_choice, attrs={'class':'form-control anaemia'}))
    anaemia_remarks = forms.CharField(label=_("Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control anaemia_remarks_val', 'placeholder':_('')})) 
    oedema = forms.CharField(required=False, label='Oedema', widget=forms.Select(choices=Oedema_choice, attrs={'class':'form-control oedema'}))
    oedema_remarks = forms.CharField(label=_("Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control oedema_remarks_val', 'placeholder':_('')})) 
    lymphadenopathy = forms.CharField(required=False, label='Lymphadenopathy', widget=forms.Select(choices=Lymphadenopathy_choice, attrs={'class':'form-control lymphadenopathy'}))
    lymphadenopathy_remarks = forms.CharField(label=_("Lymphadenopathy Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control lymphadenopathy_remarks_val', 'placeholder':_('')})) 
    clubbing = forms.CharField(required=False, label='Clubbing', widget=forms.Select(choices=Clubbing_choice, attrs={'class':'form-control clubbing'}))
    clubbing_remarks = forms.CharField(label=_("Remarks"), required=False,  widget=forms.TextInput(attrs={'class':'form-control clubbing_remarks_val', 'placeholder':_('')})) 
 
    
    class Meta:
            model = GeneralExamination
            fields = (
                'blood_pressure','pulse','respiratory_rate','cyanosis','cyanosis_remarks',
                'jaundice','jaundice_remarks','anaemia','anaemia_remarks','oedema','oedema_remarks',
                'lymphadenopathy','lymphadenopathy_remarks','clubbing','clubbing_remarks'
            )
#General Examination using as Embedded Field in Case Physical Examination Findings Ends Here
#Systemic Examination using as Embedded Field in Case Physical Examination Findings Starts Here
class SystemicExamination(models.Model):
    respiratory_system = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Respiratory System"))
    cvs = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("CVS"))
    nervous_system = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Nervous System"))
    gastro_intestinal_system = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Gastro Intestinal System"))
    genito_urinary_system = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Genito Urinary System"))
    locomotor_system = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Locomotor System"))
    skin = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Skin"))
    others = models.TextField(blank=True, null=True, verbose_name=_("Others"))

    def __str__(self):
        return self.respiratory_system
   
    class Meta:
        abstract = True

class SystemicExaminationForm(forms.ModelForm):
    respiratory_system = forms.CharField(label=_("Respiratory System"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control respiratory_system', 'placeholder':_('')})) 
    cvs = forms.CharField(label=_("CVS"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control cvs', 'placeholder':_('')})) 
    nervous_system = forms.CharField(label=_("Nervous System"), required=False,  widget=forms.TextInput(attrs={'class':'form-control nervous_system', 'placeholder':_('')})) 
    gastro_intestinal_system = forms.CharField(label=_("Gastro Intestinal System"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control gastro_intestinal_system', 'placeholder':_('')})) 
    genito_urinary_system = forms.CharField(label=_("Genito Urinary System"), required=False,  widget=forms.TextInput(attrs={'class':'form-control genito_urinary_system', 'placeholder':_('')})) 
    locomotor_system = forms.CharField(label=_("Locomotor System"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control locomotor_system', 'placeholder':_('')})) 
    skin = forms.CharField(label=_("Skin"), required=False,  widget=forms.TextInput(attrs={'class':'form-control skin', 'placeholder':_('')})) 
    others = forms.CharField(label=_("Others"), required=False,  widget=forms.TextInput(attrs={'class':'form-control others', 'placeholder':_('')})) 

    class Meta:
            model = SystemicExamination
            fields = (
                'respiratory_system','cvs','nervous_system','gastro_intestinal_system',
                'genito_urinary_system','locomotor_system','skin','others',
            )
#Systemic Examination using as Embedded Field in Case Physical Examination Findings Ends Here
class CasePhysicalExaminationFindings(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    general_examination = models.EmbeddedField(
        model_container = GeneralExamination,
        model_form_class = GeneralExaminationForm,
    )
    systemic_examination = models.EmbeddedField(
        model_container = SystemicExamination,
        model_form_class = SystemicExaminationForm,
        null = True
    )
    def __str__(self):
        return self.case.case_title
   
    class Meta:
        verbose_name = "Case Physical Examination Findings"
        verbose_name_plural = "Case Physical Examination Findings"
        db_table = 'ccrh_case_phy_examination_finding'
#Case Physical Examination Findings Model Ends Here


#Case Gynaecological History Model Starts Here 
#Menarche using as Array Field in Case Personal History Starts Here
class Menarche(models.Model):
    age = models.IntegerField(blank=True, null=True, verbose_name=_("Age"))
    date = models.DateTimeField(blank=True, null=True, verbose_name=_("date"))
    related_complaints_during = models.TextField(blank=True, null=True, verbose_name=_("Related Complaints During"))    

    def __str__(self):
        return self.age
    
    class Meta:
        abstract = True

class MenarcheForm(forms.ModelForm):
    age = forms.IntegerField(label=_("Age"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    date = forms.DateTimeField(label=_("Date"), required=False, input_formats=['%Y-%m-%d'], widget=forms.DateTimeInput(format = '%Y-%m-%d',attrs={'class':'form-control from_date date_picker'}))
    related_complaints_during = forms.CharField(label=_("Related Complaints During"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    class Meta:
            model = Menarche
            fields = (
                'age','date','related_complaints_during'
            )
#Menarche using as Array Field in Case Personal History Model Ends Here

#Menstrual Cycle Particulars Methods using as Array Field in Case Personal History Model Starts Here
#Lmp using as Array Field in Case Personal History Starts Here
class Lmp(models.Model):
    date = models.DateTimeField(blank=True, null=True, verbose_name=_("date"))

    def __str__(self):
        return self.date
    
    class Meta:
        abstract = True

class LmpForm(forms.ModelForm):
    date = forms.DateTimeField(label=_("Date"), required=False, input_formats=['%Y-%m-%d'], widget=forms.DateTimeInput(format = '%Y-%m-%d',attrs={'class':'form-control from_date date_picker',}))

    class Meta:
        model = Lmp
        fields = ('date',)
#Lmp using as Array Field in Case Personal History Model Ends Here
#Bleeding using as Array Field in Case Personal History Starts Here
class Bleeding(models.Model):
    days = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("days"))
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("quantity"))

    def __str__(self):
        return self.days
    
    class Meta:
        abstract = True

class BleedingForm(forms.ModelForm):
    Quantity_CHOICES= (
        (u'', u'Select'),
        (u'Profuse', u'Profuse'),
        (u'Scanty', u'Scanty'),
        (u'Normal', u'Normal'),
    )
    days = forms.CharField(label=_("Days"), required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    quantity = forms.CharField(label=_("Quantity"), max_length=250, required=False, widget=forms.Select(choices=Quantity_CHOICES, attrs={'class':'form-control'})) 
    
    class Meta:
        model = Bleeding
        fields = ('days','quantity')
#Bleeding using as Array Field in Case Personal History Model Ends Here
#Cycle using as Array Field in Case Personal History Starts Here
class Cycle(models.Model):
    cycle = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("cycle"), help_text=_("Values will be stored as Regular, Irregular"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("remarks"))

    def __str__(self):
        return self.cycle
    
    class Meta:
        abstract = True

class CycleForm(forms.ModelForm):
    CYCLE_CHOICES= (
        (u'', u'Select'),
        (u'Regular', u'Regular'),
        (u'Irregular', u'Irregular'),
    )
    cycle = forms.CharField(label=_("Cycle"), max_length=250, required=False, widget=forms.Select(choices=CYCLE_CHOICES, attrs={'class':'form-control'})) 
    remarks = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control cycle_remarks_value','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Cycle
        fields = ('cycle','remarks')
#Cycle using as Array Field in Case Personal History Model Ends Here
#Colour using as Array Field in Case Personal History Starts Here
class Colour(models.Model):
    colour = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Colour"), help_text=_("Values will be stored as Bright red, Dark red, Black, Pale"))
    other_remarks = models.TextField(blank=True, null=True, verbose_name=_("remarks"))

    def __str__(self):
        return self.colour
    
    class Meta:
        abstract = True
        
class ColourForm(forms.ModelForm):
    COLOUR_CHOICES= (
        (u'', u'Select'),
        (u'Bright red', u'Bright red'),
        (u'Dark red', u'Dark red'),
        (u'Black', u'Black'),
        (u'Pale', u'Pale'),
        (u'Other', u'Other'),
    )
    colour = forms.CharField(label=_("Colour"), max_length=250, required=False, widget=forms.Select(choices=COLOUR_CHOICES, attrs={'class':'form-control'})) 
    other_remarks = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control colour_remarks_value','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Colour
        fields = ('colour','other_remarks')
#Colour using as Array Field in Case Personal History Model Ends Here
#Consistency using as Array Field in Case Personal History Starts Here
class Consistency(models.Model):
    consistency = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Consistency"))

    def __str__(self):
        return self.consistency
    
    class Meta:
        abstract = True
        
class ConsistencyForm(forms.ModelForm):
    CONSISTENCY_CHOICES= (
        (u'Fluid', u'Fluid'),
        (u'Clotted', u'Clotted'),
        (u'Mixed', u'Mixed'),
        (u'Thick', u'Thick'),
        (u'Thin', u'Thin'),
        (u'Stringy', u'Stringy'),
    )
    consistency = forms.MultipleChoiceField(label=_("Consistency"), required=False, choices=CONSISTENCY_CHOICES,widget=forms.SelectMultiple( attrs={'class':'form-control consistency_val select_container'})) 

    class Meta:
        model = Consistency
        fields = ('consistency',)
#Consistency using as Array Field in Case Personal History Model Ends Here
#Odour using as Array Field in Case Personal History Starts Here
class Odour(models.Model):
    odour = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Odour"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("remarks"))

    def __str__(self):
        return self.odour
    
    class Meta:
        abstract = True

class OdourForm(forms.ModelForm):
    ODOUR_CHOICES= (
        (u'', u'Select'),
        (u'Odourless', u'Odourless'),
        (u'Offensive', u'Offensive'),
    )
    odour = forms.CharField(label=_("Odour"), max_length=250, required=False, widget=forms.Select(choices=ODOUR_CHOICES, attrs={'class':'form-control odour_mentstr'})) 
    remarks = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control odur_remarks_value','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Odour
        fields = ('odour','remarks')
#Odour using as Array Field in Case Personal History Model Ends Here
#Character using as Array Field in Case Personal History Starts Here
class Character(models.Model):
    character = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Character"), help_text=_("Values will be stored as Acrid, Bland"))
    other_remarks = models.TextField(blank=True, null=True, verbose_name=_("remarks"))

    def __str__(self):
        return self.character
    
    class Meta:
        abstract = True

class CharacterForm(forms.ModelForm):
    CHARACTER_CHOICES= (
        (u'', u'Select'),
        (u'Acrid', u'Acrid'),
        (u'Bland', u'Bland'),
        (u'Other', u'Other'),
    )
    character = forms.CharField(label=_("Character"), max_length=250, required=False, widget=forms.Select(choices=CHARACTER_CHOICES, attrs={'class':'form-control'})) 
    other_remarks = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control character_remarks_value','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Character
        fields = ('character','other_remarks')
#Character using as Array Field in Case Personal History Model Ends Here
#Dysmenorrhoea using as Array Field in Case Personal History Starts Here
class Dysmenorrhoea(models.Model):
    dysmenorrhoea = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Dysmenorrhoea"), help_text=_("Values will be stored as Severe, moderate, mild "))
    complaints = models.TextField(blank=True, null=True, verbose_name=_("Complaints"))
    
    def __str__(self):
        return self.dysmenorrhoea
    
    class Meta:
        abstract = True

class DysmenorrhoeaForm(forms.ModelForm):
    DYSMENORRHOEA_CHOICES= (
        (u'', u'Select'),
        (u'Severe', u'Severe'),
        (u'Moderate', u'Moderate'),
        (u'Mild', u'Mild'),
    )
    dysmenorrhoea = forms.CharField(label=_("Dysmenorrhoea"), max_length=250, required=False, widget=forms.Select(choices=DYSMENORRHOEA_CHOICES, attrs={'class':'form-control'})) 
    complaints = forms.CharField(label=_("Complaints"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Dysmenorrhoea
        fields = ('dysmenorrhoea','complaints')
#Dysmenorrhoea using as Array Field in Case Personal History Model Ends Here
#Complaints using as Array Field in Case Personal History Starts Here
class Complaints(models.Model):
    complaints = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Complaints"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("remarks"))

    def __str__(self):
        return self.complaints
    
    class Meta:
        abstract = True

class ComplaintsForm(forms.ModelForm):
    COMPLAINTS_CHOICES= (
        (u'', u'Select'),
        (u'Before menses', u'Before menses'),
        (u'After menses', u'After menses'),
        (u'During menses', u'During menses'),
    )
    complaints = forms.CharField(label=_("Complaints"), max_length=250, required=False, widget=forms.Select(choices=COMPLAINTS_CHOICES, attrs={'class':'form-control'})) 
    remarks = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Complaints
        fields = ('complaints','remarks')
#Complaints using as Array Field in Case Personal History Model Ends Here
class MenstrualCycleParticulars(models.Model):
    lmp = models.EmbeddedField(
        model_container = Lmp,
        model_form_class = LmpForm,
        null=True
    )
    bleeding = models.EmbeddedField(
        model_container = Bleeding,
        model_form_class = BleedingForm,
        null=True
    )
    cycle = models.EmbeddedField(
        model_container = Cycle,
        model_form_class = CycleForm,
        null=True
    )
    colour = models.EmbeddedField(
        model_container = Colour,
        model_form_class = ColourForm,
        null=True
    )
    consistency = models.EmbeddedField(
        model_container = Consistency,
        model_form_class = ConsistencyForm,
        null=True
    )
    odour = models.EmbeddedField(
        model_container = Odour,
        model_form_class = OdourForm,
        null=True
    )
    character = models.EmbeddedField(
        model_container = Character,
        model_form_class = CharacterForm,
        null=True
    )
    dysmenorrhoea = models.EmbeddedField(
        model_container = Dysmenorrhoea,
        model_form_class = DysmenorrhoeaForm,
        null=True
    )
    complaints = models.ArrayField(
        model_container = Complaints,
        model_form_class = ComplaintsForm,
        null=True
    )
    def __str__(self):
        return self.lmp
    
    class Meta:
        abstract = True
        
class MenstrualCycleParticularsForm(forms.ModelForm):
    class Meta:
            model = MenstrualCycleParticulars
            fields = (
                'lmp','bleeding','cycle','colour','consistency','odour','character','dysmenorrhoea',
                'complaints'
            )
#Menstrual Cycle Particulars Methods using as Array Field in Case Personal History Model Ends Here

#Abnormal Discharge Methods using as Array Field in Case Personal History Model Starts Here
#Leucorrhea using as Array Field in Case Personal History Starts Here
class Leucorrhea(models.Model):
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Quantity"))
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("color"))
    color_others = models.TextField(blank=True, null=True, verbose_name=_("color_remarks"))
    consistency = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Consistency"))
    consistency_remarks = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    stains = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Stains"))
    odour = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Odour"))
    odour_other = models.TextField(blank=True, null=True, verbose_name=_("Odour_remarks"))
    character = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Character"))
    character_remarks = models.TextField(blank=True, null=True, verbose_name=_("Character_remarks"))
    relation_with_menses = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Relation_with_Menses"))

    def __str__(self):
        return self.quantity
    
    class Meta:
        abstract = True

class LeucorrheaForm(forms.ModelForm):
    Quantity_CHOICES= (
        (u'', u'Select'),
        (u'Profuse', u'Profuse'),
        (u'Scanty', u'Scanty'),
    )
    Color_CHOICES= (
        (u'', u'Select'),
        (u'Yellow', u'Yellow'),
        (u'Green', u'Green'),
        (u'White', u'White'),
    )
    Consistency_CHOICES= (
        (u'Thick', u'Thick'),
        (u'Thin', u'Thin'),
        (u'Stringy', u'Stringy'),
        (u'Creamy', u'Creamy'),
    )
    Stains_CHOICES= (
        (u'', u'Select'),
        (u'Difficult to wash', u'Difficult to wash'),
        (u'Yellow', u'Yellow'),
        (u'Dirty', u'Dirty'),
    )
    Odur_CHOICES= (
        (u'', u'Select'),
        (u'Odourless', u'Odourless'),
        (u'Offensive', u'Offensive'),
    )
    Character_CHOICES= (
        (u'', u'Select'),
        (u'Acrid', u'Acrid'),
        (u'Bland', u'Bland'),
        (u'Corrodes', u'Corrodes'),
        (u'Linen', u'Linen'),
    ) 
    Relation_with_Menses_CHOICES= (
        (u'', u'Select'),
        (u'Before', u'Before'),
        (u'During', u'During'),
        (u'After', u'After'),
    ) 
    quantity = forms.CharField(label=_("Quantity"), max_length=250, required=False, widget=forms.Select(choices=Quantity_CHOICES, attrs={'class':'form-control'})) 
    color = forms.CharField(label=_("Color"), max_length=250, required=False, widget=forms.Select(choices=Color_CHOICES, attrs={'class':'form-control'})) 
    color_others = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    consistency = forms.MultipleChoiceField(label=_("Consistency"), required=False, choices=Consistency_CHOICES,widget=forms.SelectMultiple( attrs={'class':'form-control leuca_consistency select_container'})) 
    consistency_remarks = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    stains = forms.CharField(label=_("Stains"), max_length=250, required=False, widget=forms.Select(choices=Stains_CHOICES, attrs={'class':'form-control'})) 
    odour = forms.CharField(label=_("Odour"), max_length=250, required=False, widget=forms.Select(choices=Odur_CHOICES, attrs={'class':'form-control leuco_odour'})) 
    odour_other = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control leuco_odur_remarks_value','rows':'3', 'cols':'25',})) 
    character = forms.CharField(label=_("Character"), max_length=250, required=False, widget=forms.Select(choices=Character_CHOICES, attrs={'class':'form-control'})) 
    character_remarks = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    relation_with_menses = forms.CharField(label=_("Relation With Menses"), max_length=250, required=False, widget=forms.Select(choices=Relation_with_Menses_CHOICES, attrs={'class':'form-control'})) 
    class Meta:
            model = Leucorrhea
            fields = (
                'quantity','color','color_others','consistency','consistency_remarks','stains','odour','odour_other','character','character_remarks','relation_with_menses'
            )
#Leucorrhea using as Array Field in Case Personal History Model Ends Here
#Bleeding Per Vagina using as Array Field in Case Personal History Starts Here
class BleedingPerVagina(models.Model):
    quantity = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Quantity"))
    color = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("color"))
    color_others = models.TextField(blank=True, null=True, verbose_name=_("color_remarks"))
    consistency = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Consistency"))
    consistency_remarks = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    stains = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Stains"))
    odour = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Odour"))
    odour_other = models.TextField(blank=True, null=True, verbose_name=_("Odour_remarks"))
    character = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Character"))
    character_remarks = models.TextField(blank=True, null=True, verbose_name=_("Character_remarks"))
    relation_with_menses = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Relation_with_Menses"))

    def __str__(self):
        return self.quantity
    
    class Meta:
        abstract = True

class BleedingPerVaginaForm(forms.ModelForm):
    Quantity_CHOICES= (
        (u'', u'Select'),
        (u'Profuse', u'Profuse'),
        (u'Scanty', u'Scanty'),
    )
    Color_CHOICES= (
        (u'', u'Select'),
        (u'Bright red', u'Bright red'),
        (u'Dark red', u'Dark red'),
        (u'Black', u'Black'),
        (u'Pale', u'Pale'),
    )
    Consistency_CHOICES= (
        (u'Fluid', u'Fluid'),
        (u'Clotted', u'Clotted'),
        (u'Mixed', u'Mixed'),
        (u'Thick', u'Thick'),
        (u'Thin', u'Thin'),
        (u'Stringy', u'Stringy'),
    )
    Stains_CHOICES= (
        (u'', u'Select'),
        (u'Difficult to wash', u'Difficult to wash'),
    )
    Odur_CHOICES= (
        (u'', u'Select'),
        (u'Odourless', u'Odourless'),
        (u'Offensive', u'Offensive'),
    )
    Character_CHOICES= (
        (u'', u'Select'),
        (u'Acrid', u'Acrid'),
        (u'Bland', u'Bland'),
        (u'Corrodes', u'Corrodes'),
        (u'Linen', u'Linen'),
    ) 
    Relation_with_Menses_CHOICES= (
        (u'', u'Select'),
        (u'Before', u'Before'),
        (u'After', u'After'),
    ) 
    quantity = forms.CharField(label=_("Quantity"), max_length=250, required=False, widget=forms.Select(choices=Quantity_CHOICES, attrs={'class':'form-control'})) 
    color = forms.CharField(label=_("Color"), max_length=250, required=False, widget=forms.Select(choices=Color_CHOICES, attrs={'class':'form-control'})) 
    color_others = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    consistency = forms.MultipleChoiceField(label=_("Consistency"), required=False, choices=Consistency_CHOICES,widget=forms.SelectMultiple( attrs={'class':'form-control bleed_consistency select_container'})) 
    consistency_remarks = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    stains = forms.CharField(label=_("Stains"), max_length=250, required=False, widget=forms.Select(choices=Stains_CHOICES, attrs={'class':'form-control'})) 
    odour = forms.CharField(label=_("Odour"), max_length=250, required=False, widget=forms.Select(choices=Odur_CHOICES, attrs={'class':'form-control bleed_odour'})) 
    odour_other = forms.CharField(label=_("Remarks"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control bleed_odur_remarks_value','rows':'3', 'cols':'25',})) 
    character = forms.CharField(label=_("Character"), max_length=250, required=False, widget=forms.Select(choices=Character_CHOICES, attrs={'class':'form-control'})) 
    character_remarks = forms.CharField(label=_("Description"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    relation_with_menses = forms.CharField(label=_("Relation With Menses"), max_length=250, required=False, widget=forms.Select(choices=Relation_with_Menses_CHOICES, attrs={'class':'form-control'})) 
    class Meta:
            model = BleedingPerVagina
            fields = (
                'quantity','color','color_others','consistency','consistency_remarks','stains','odour','odour_other','character','character_remarks','relation_with_menses'
            )
#Bleeding Per Vagina using as Array Field in Case Personal History Model Ends Here
class AbnormalDischarge(models.Model):
    leucorrhea = models.EmbeddedField(
        model_container = Leucorrhea,
        model_form_class = LeucorrheaForm,
        null=True
    )
    bleeding_per_vagina = models.EmbeddedField(
        model_container = BleedingPerVagina,
        model_form_class = BleedingPerVaginaForm,
        null=True
    )
    def __str__(self):
        return self.leucorrhea
    
    class Meta:
        abstract = True
        
class AbnormalDischargeForm(forms.ModelForm):
    class Meta:
            model = AbnormalDischarge
            fields = (
                'leucorrhea','bleeding_per_vagina'
            )
#Abnormal Discharge Methods using as Array Field in Case Personal History Model Ends Here

#Menopause using as Array Field in Case Personal History Starts Here
class Menopause(models.Model):
    age = models.IntegerField(blank=True, null=True, verbose_name=_("Age"))
    associated_complaints = models.TextField(blank=True, null=True, verbose_name=_("Associated Complaints"))

    def __str__(self):
        return self.age
    
    class Meta:
        abstract = True

class MenopauseForm(forms.ModelForm):
    age = forms.IntegerField(label=_("Age"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    associated_complaints = forms.CharField(label=_("Associated Complaints"), max_length=1000, required=False, widget=forms.HiddenInput(attrs={'class':'form-control',})) 

    class Meta:
            model = Menopause
            fields = (
                'age','associated_complaints'
            )
#Menopause using as Array Field in Case Personal History Model Ends Here

#HoGynaecologicalSurgeries Methods using as Array Field in Case Personal History Model Ends Here
#Hysterectomy using as Array Field in Case Personal History Starts Here
class Hysterectomy(models.Model):
    hysterectomy = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Hysterectomy"))
    reason = models.TextField(blank=True, null=True, verbose_name=_("Reason"))
    age = models.IntegerField(blank=True, null=True, verbose_name=_("Age"))

    def __str__(self):
        return self.hysterectomy
    
    class Meta:
        abstract = True

class HysterectomyForm(forms.ModelForm):
    Hysterectomy_CHOICES= (
        (u'', u'Select'),
        (u'Yes', u'Yes'),
        (u'No', u'No'),
    )
    hysterectomy = forms.CharField(label=_("Hysterectomy"), max_length=250, required=False, widget=forms.Select(choices=Hysterectomy_CHOICES, attrs={'class':'form-control',})) 
    reason = forms.CharField(label=_("Reason"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    age = forms.IntegerField(label=_("Age"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
            model = Hysterectomy
            fields = (
                'hysterectomy','reason','age'
            )
#Hysterectomy using as Array Field in Case Personal History Model Ends Here
#Others using as Array Field in Case Personal History Starts Here
class Others(models.Model):
    others = models.TextField(blank=True, null=True, verbose_name=_("Others"))
    reason = models.TextField(blank=True, null=True, verbose_name=_("Reason"))
    age = models.IntegerField(blank=True, null=True, verbose_name=_("Age"))    

    def __str__(self):
        return self.others
    
    class Meta:
        abstract = True

class OthersForm(forms.ModelForm):
    others = forms.CharField(label=_("Others"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control',})) 
    reason = forms.CharField(label=_("Reason"), max_length=250, required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 
    age = forms.IntegerField(label=_("Age"), required=False, widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
            model = Others
            fields = (
                'others','reason','age'
            )
#Others using as Array Field in Case Personal History Model Ends Here
class HoGynaecologicalSurgeries(models.Model):
    hysterectomy = models.EmbeddedField(
        model_container = Hysterectomy,
        model_form_class = HysterectomyForm,
        null=True
    )
    others = models.ArrayField(
        model_container = Others,
        model_form_class = OthersForm,
        null=True
    )
    def __str__(self):
        return self.hysterectomy
    
    class Meta:
        abstract = True
        
class HoGynaecologicalSurgeriesForm(forms.ModelForm):
    class Meta:
            model = HoGynaecologicalSurgeries
            fields = (
                'hysterectomy','others'
            )
#HoGynaecologicalSurgeries Methods using as Array Field in Case Personal History Model Ends Here

#Contraceptive Methods using as Array Field in Case Personal History Starts Here
class ContraceptiveMethods(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Type"))
    complaints_from = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Complaints From"))

    def __str__(self):
        return self.type
    
    class Meta:
        abstract = True

class ContraceptiveMethodsForm(forms.ModelForm):
    type = forms.CharField(label=_("Type"), max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control',})) 
    complaints_from = forms.CharField(label=_("Complaints From"), max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control',})) 

    class Meta:
            model = ContraceptiveMethods
            fields = (
                'type','complaints_from',
            )
#Contraceptive Methods using as Array Field in Case Personal History Model Ends Here


class CaseGynaecologicalHistory(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    menarche = models.EmbeddedField(
        model_container = Menarche,
        model_form_class = MenarcheForm,
        null=True
    )
    menstrual_cycle_particulars = models.EmbeddedField(
        model_container = MenstrualCycleParticulars,
        model_form_class = MenstrualCycleParticularsForm,
        null=True
    )
    abnormal_discharge = models.EmbeddedField(
        model_container = AbnormalDischarge,
        model_form_class = AbnormalDischargeForm,
        null=True
    )
    menopause = models.EmbeddedField(
        model_container = Menopause,
        model_form_class = MenopauseForm,
        null=True
    )
    ho_gynaecological_surgeries = models.EmbeddedField(
        model_container = HoGynaecologicalSurgeries,
        model_form_class = HoGynaecologicalSurgeriesForm,
        null=True
    )
    contraceptive_methods = models.ArrayField(
        model_container = ContraceptiveMethods,
        model_form_class = ContraceptiveMethodsForm,
        null=True
    )
    
    def __str__(self):
        return self.case.case_title
    
    class Meta:
        verbose_name = "Case Gynaecological History"
        verbose_name_plural = "Case Gynaecological History"
        db_table = 'ccrh_case_gynae_history'
#Case Gynaecological History Model Ends Here 

#Case Repertorisation Model Ends here
#Symptoms Repertorized using as ArrayField in Case Repertorisation Model Starts here    
class SymptomsRepertorized(models.Model):
    symptoms_repertor = models.TextField(verbose_name=_("Symptoms Repertorized"))

#     symptoms_repertor = models.ForeignKey(SymptomsMaster, blank=True,null=True, on_delete=models.CASCADE, verbose_name=_("Symptoms Repertorized"))

    def __str__(self):
        return self.symptoms_repertor
    
    class Meta:
        abstract = True

class SymptomsRepertorizedForm(forms.ModelForm):
    symptoms_repertor = forms.CharField(label=_("Description"), max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control',})) 
#     symptoms_repertor = forms.ModelChoiceField(label=_("Description"),
#         queryset=SymptomsMaster.objects.all(),
#         widget=autocomplete.ModelSelect2(url='case_history:symptoms-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
#     )
    class Meta:
        model = SymptomsRepertorized
        fields = (
            'symptoms_repertor',
        )
#Symptoms Repertorized using as ArrayField in Case Repertorisation Model Ends here
#Medicine using as ArrayField in Case Repertorisation Model Starts here    
class Medicine(models.Model):
    medicine = models.ForeignKey(MedicineMaster, blank=True,null=True, on_delete=models.CASCADE, verbose_name=_("Medicine"))
    marks = models.TextField(blank=True,null=True, verbose_name=_("Marks"))
    
    def __str__(self):
        return self.medicine.med_name
    
    class Meta:
        abstract = True

class MedicineForm(forms.ModelForm):
    medicine = forms.ModelChoiceField(label=_("Medicine Name"),
        queryset=MedicineMaster.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:medicine-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    marks = forms.CharField(label=_("Marks"), required=False, widget=forms.Textarea(attrs={'class':'form-control','rows':'3', 'cols':'25',})) 

    class Meta:
        model = Medicine
        fields = (
            'medicine','marks',
        )
#Medicine using as ArrayField in Case Repertorisation Model Ends here    

class CaseRepertorisation(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    computerized_manual_report = models.FileField(upload_to='Repertorisation_Upload/',verbose_name=_("Computerized / Manual Report"))
    symptoms_repertorized = models.ArrayField(
        model_container=SymptomsRepertorized,
        model_form_class = SymptomsRepertorizedForm,
        null = True 
    )
    medicines = models.ArrayField(
        model_container=Medicine,
        model_form_class = MedicineForm,
        null = True
    )
     
    def __str__(self):
         return self.case.case_title
     
    class Meta:
        verbose_name = "Case Repertorisation "
        verbose_name_plural = "Case Repertorisation "
        db_table = 'ccrh_case_repertorisation'
#Case Repertorisation Model Ends here

# Case Miasamatic Analysis Model Ends here
#Predominant Miasm using as ArrayField in Case Miasamatic Analysis Starts here    
class PredominantMiasm(models.Model):
    predominant_miasm = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("Predominant Miasm"))
    remarks = models.TextField(blank=True,null=True,  verbose_name=_("Remarks"))
     
    def __str__(self):
         return self.predominant_miasm
     
    class Meta:
         abstract = True
         
#Predominant Miasm using as ArrayField in Case Miasamatic Analysis Ends here
class CaseMiasamaticAnalysis(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    predominant_miasm = models.ArrayField(
        model_container=PredominantMiasm,
        null = True 
     )
    class Meta:
        verbose_name = "Case Miasamatic Analysis"
        verbose_name_plural = "Case Miasamatic Analysis"
        db_table = 'ccrh_case_miasamatic_analysis'
#Case Miasamatic Analysis Model Ends here

# '''Case Obstetric History models start here'''
# Previous Pregnancies using as Array Field in Case Obstetric History start Here        
class ObstetricHistory(models.Model):
    prev_pregnancies =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Previous Pregnancies") ,help_text=_("Values will be stored as"))
    value = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Value"))
    def __str__(self):
        return self.prev_pregnancies
 
    class Meta:
        abstract = True
 
class ObstetricHistoryForm(forms.ModelForm):
    prev_pregnancies_CHOICES= (
        (u'', u'Select'),
        (u'Gravida', u'Gravida'),
        (u'Para', u'Para'),
        (u'Abortion', u'Abortion'),
        (u'Stillbirth', u'Stillbirth'),
        (u'Living', u'Living'),
    )
    prev_pregnancies = forms.CharField(label=_("Previous Pregnancies"),required=False, max_length=250, widget=forms.Select(choices=prev_pregnancies_CHOICES, attrs={'class':'form-control mothers_milk', 'placeholder':_('')})) 
    value = forms.CharField(label=_("Value"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
 
    class Meta:
            model = ObstetricHistory
            fields = ('prev_pregnancies','value')  
# Previous Pregnancies using as Array Field in Case Obstetric History ends Here

class ComplaintsDuringPregnancy(models.Model):
    comp_during_pregnancy = models.ForeignKey(DiseaseMaster, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Complaints During Pregnancy"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
 
    def __str__(self):
        return self.remarks
 
    class Meta:
        abstract = True
 
class ComplaintsDuringPregnancyForm(forms.ModelForm):
#     comp_during_pregnancy=forms.ModelChoiceField(label=_("Complaints During Pregnancy"),
#        queryset=State.objects.all(),
#        widget=autocomplete.ModelSelect2Multiple(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2,'data-maximum-selection-length':10})
#     )
    comp_during_pregnancy = forms.ModelChoiceField(label=_("Complaints During Pregnancy"),
        queryset=DiseaseMaster.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    remarks = forms.CharField(label=_("Remarks"), required=False, max_length=250, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':_('')})) 
 
    class Meta:
            model = ComplaintsDuringPregnancy
            fields = ('comp_during_pregnancy','remarks')
             
class NatureOfLabor(models.Model):
    nature_of_labor = models.ForeignKey(DiseaseMaster, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Nature Of Labor"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("Remarks"))
 
    def __str__(self):
        return self.nature_of_labor
 
    class Meta:
        abstract = True
 
class NatureOfLaborForm(forms.ModelForm):
    nature_of_labor = forms.ModelChoiceField(label=_("Nature Of Labor"),
        queryset=DiseaseMaster.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    remarks = forms.CharField(label=_("Remarks"), required=False, max_length=250, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':_('')})) 
 
    class Meta:
            model = NatureOfLabor
            fields = ('nature_of_labor','remarks')
            
 # Antenatal using as Array Field in Case Obstetric History start Here      
class Antenatal(models.Model):
    period_of_pregnancy = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Period Of Pregnancy"))
    complaints_during_pregnancy = models.ArrayField(
        model_container = ComplaintsDuringPregnancy,
        model_form_class = ComplaintsDuringPregnancyForm,
        null=True
    )
    nature_of_labor = models.EmbeddedField(
        model_container = NatureOfLabor,
        model_form_class = NatureOfLaborForm,
        null=True
    )
    nature_of_delivery = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Nature Of Delivery"))
    nature_of_delivery_normal = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Nature Of Delivery Normal"))
     
    def __str__(self):
        return self.period_of_pregnancy
 
    class Meta:
        abstract = True
 
class AntenatalForm(forms.ModelForm):
    period_of_pregnancy = forms.CharField(label=_("Period Of Pregnancy"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    nature_of_delivery = forms.CharField(label=_("Nature Of Delivery"), required=False, max_length=250, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    class Meta:
            model = Antenatal
            fields = ('period_of_pregnancy','complaints_during_pregnancy','nature_of_labor','nature_of_delivery')   
 # Postnatal using as Array Field in Case Obstetric History end Here
 
 # Postnatal using as Array Field in Case Obstetric History start Here
class Postnatal(models.Model):
    nature_of_puerperium = models.ForeignKey(DiseaseMaster, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Period Of Pregnancy"))
    remarks = models.TextField(blank=True, null=True, verbose_name=_("Nature Of Delivery"))
     
    def __str__(self):
        return self.nature_of_puerperium
 
    class Meta:
        abstract = True
 
class PostnatalForm(forms.ModelForm):
    nature_of_puerperium = forms.ModelChoiceField(label=_("Nature Of Puerperium"),
        queryset=DiseaseMaster.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    remarks = forms.CharField(label=_("Remarks"), required=False, max_length=250, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':_('')})) 
    class Meta:
            model = Postnatal
            fields = ('nature_of_puerperium','remarks')   
# Postnatal using as Array Field in Case Obstetric History end Here       
     
# Child using as Array Field in Case Obstetric History start Here
class Child(models.Model):
    alive =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Alive"))
    cause_of_death = models.ForeignKey(DiseaseMaster, blank=True, null=True, on_delete=models.CASCADE, verbose_name=_("Cause Of Death"))
    birth_weight =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Birth Weight"))
    lactation_history =  models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Lactation History"))
    
    def __str__(self):
        return self.alive
 
    class Meta:
        abstract = True
 
 
class ChildForm(forms.ModelForm):
    Alive_CHOICES= (
        (u'', u'Select'),
        (u'Yes', u'Yes'),
        (u'No', u'No'),
    )
    alive = forms.CharField(label=_("Alive"), required=False, max_length=250, widget=forms.Select(choices=Alive_CHOICES, attrs={'class':'form-control', 'placeholder':_('')})) 
    cause_of_death = forms.ModelChoiceField(label=_("Cause Of Death"),
        queryset=DiseaseMaster.objects.all(),required=False,
        widget=autocomplete.ModelSelect2(url='case_history:disease-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
    )
    birth_weight = forms.CharField(label=_("Birth Weight"), required=False, max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':_('')})) 
    lactation_history = forms.CharField(label=_("Lactation History"), required=False, max_length=300, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':_('')})) 
    
    class Meta:
            model = Child
            fields = ('alive','cause_of_death','birth_weight','lactation_history') 
# Child using as Array Field in Case Obstetric History start Here
             
# Pregnancy using as Array Field in Case Obstetric History start Here      
class Pregnancy(models.Model):
    antenatal = models.EmbeddedField(
        model_container = Antenatal,
        model_form_class = AntenatalForm,
    )
    postnatal = models.EmbeddedField(
        model_container = Postnatal,
        model_form_class = PostnatalForm,
        null=True
    )
    child = models.ArrayField(
        model_container = Child,
        model_form_class = ChildForm,
        null=True
    )
    def __str__(self):
        return self.child
 
    class Meta:
        abstract = True
 
class PregnancyForm(forms.ModelForm):
    class Meta:
            model = Pregnancy
            fields = ('antenatal','postnatal','child')   
 # Pregnancy using as Array Field in Case Obstetric History End Here
             
class CaseObstetricHistory(models.Model):
    _id = models.ObjectIdField()
    case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
    previous_pregnancies = models.ArrayField(
        model_container = ObstetricHistory,
        model_form_class = ObstetricHistoryForm,
        null=True
    )
    pregnancy = models.ArrayField(
        model_container = Pregnancy,
        model_form_class = PregnancyForm,
        null=True
    )
    def __str__(self):
        return self.case
    
    class Meta:
        verbose_name = "Case Obstetric History"
        verbose_name_plural = "Case Obstetric History"
        db_table = 'ccrh_case_obstetric_history'
         
# '''Case Obstetric History models ends here'''
'''Finalize case history models ends here'''








# '''Follow Up Practitioners models Starts here'''
# class MedicineFollowUpPract(models.Model):
#     prescription = models.ForeignKey(MedicineMaster, blank=True,null=True, on_delete=models.CASCADE, verbose_name=_("Medicine"))
#     potency = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Potency"))
#     dosages = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Dosages"))
# 
#     def __str__(self):
#         return self.potency
#     
#     class Meta:
#         abstract = True
#         
# class MedicineFollowUpPractForm(forms.ModelForm):
#     prescription = forms.ModelChoiceField(label=_("Prescription"),
#         queryset=MedicineMaster.objects.all(),required=False,
#         widget=autocomplete.ModelSelect2(url='case_history:medicine-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
#     )
#     potency = forms.CharField(label=_("Potency"), required=False, widget=forms.TextInput(attrs={'class':'form-control',}))
#     dosages = forms.CharField(label=_("Dosages"), required=False, widget=forms.TextInput(attrs={'class':'form-control',}))
# 
#     class Meta:
#         model = MedicineFollowUpPract
#         fields = ('prescription','potency','dosages',)
#                     
# class SymptomsFollowUpPract(models.Model):
#     symptom = models.ForeignKey(SymptomsMaster, blank=True,null=True, on_delete=models.CASCADE, verbose_name=_("Symptoms"))
#     outcome_of_previous_prescription = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Outcome of Previous Prescription"))
#     
#     def __str__(self):
#         return self.outcome_of_previous_prescription
#     
#     class Meta:
#         abstract = True
# 
# class SymptomsFollowUpPractForm(forms.ModelForm):
#     Outcome_of_Previous_Prescription_CHOICES= (
#         (u'', u'Select'),
#         (u'Ggravation', u'Ggravation'),
#         (u'Amelioration', u'Amelioration'),
#         (u'No change', u'No change'),
#     )
#     symptom = forms.ModelChoiceField(label=_("Symptoms"),
#         queryset=SymptomsMaster.objects.all(),required=False,
#         widget=autocomplete.ModelSelect2(url='case_history:symptoms-autocomplete' ,attrs={'class':'form-control', 'data-placeholder': 'Select', 'data-minimum-input-length': 2})
#     )
#     outcome_of_previous_prescription = forms.CharField(label=_("Outcome of Previous Prescription"), max_length=250, required=False, widget=forms.Select(choices=Outcome_of_Previous_Prescription_CHOICES, attrs={'class':'form-control'})) 
# 
#     class Meta:
#         model = SymptomsFollowUpPract
#         fields = ('symptom','outcome_of_previous_prescription',)
# 
# class PatientOutcome(models.Model):
#     scale = models.CharField(max_length=250, blank=True, null=True, verbose_name=_("Scale"))
#     other_scale = models.TextField(blank=True,null=True, verbose_name=_("Other Scale"))
#     score = models.TextField(blank=True,null=True, verbose_name=_("Score"))
#     
#     def __str__(self):
#         return self.scale
#     
#     class Meta:
#         abstract = True
# 
# class PatientOutcomeForm(forms.ModelForm):
#     Scale_CHOICES= (
#         (u'', u'Select'),
#         (u'ORIDL', u'ORIDL'),
#         (u'MYMOP', u'MYMOP'),
#         (u'WHOBREF', u'WHOBREF'),
#         (u'Other', u'Other'),
#     )
#     scale = forms.CharField(label=_("Scale"), max_length=250, required=False, widget=forms.Select(choices=Scale_CHOICES, attrs={'class':'form-control'})) 
#     other_scale = forms.CharField(label=_("Other Scale"), max_length=250, required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
#     score = forms.CharField(label=_("Score"), max_length=250, required=False, widget=forms.TextInput(attrs={'class':'form-control'})) 
# 
#     class Meta:
#         model = PatientOutcome
#         fields = ('scale','other_scale','score',)
#          
# # Follow Up Practitioner using as Array Field in Case Follow Up Practitioner Start Here      
# class FollowUpPract(models.Model):
#     date = models.DateTimeField(blank=True, null=True, verbose_name=_("Date"))
#     medicine = models.ArrayField(
#         model_container = MedicineFollowUpPract,
#         model_form_class = MedicineFollowUpPractForm,
#         null=True
#     )
#     symptoms = models.ArrayField(
#         model_container = SymptomsFollowUpPract,
#         model_form_class = SymptomsFollowUpPractForm,
#         null=True
#     )
#     
#     patient_outcome = models.EmbeddedField(
#         model_container = PatientOutcome,
#         model_form_class = PatientOutcomeForm,
#         null=True
#     )
#     follow_up_order =  models.IntegerField(verbose_name=_("Follow up Order"))
#     
#     def __str__(self):
#         return str(self.follow_up_order)
#  
#     class Meta:
#         abstract = True
#  
# class FollowUpPractForm(forms.ModelForm):
#     class Meta:
#             model = FollowUpPract
#             fields = ('date','medicine','symptoms','patient_outcome','follow_up_order')   
# # Follow Up Practitioner using as Array Field in Case Follow Up Practitioner Ends Here      
# 
# class CaseFollowUpPract(models.Model):
#     _id = models.ObjectIdField()
#     case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
#     follow_up = models.ArrayField(
#         model_container = FollowUpPract,
#         model_form_class = FollowUpPractForm,
#         null=True
#     )
#     def __str__(self):
#         return self.case
#     
#     class Meta:
#         verbose_name = "Follow Up Practitioners"
#         verbose_name_plural = "Follow Up Practitioners"
#         db_table = 'ccrh_case_followup_pract'
#          
# '''Follow Up Practitioners models Ends here'''






     
# class CaseStatus(models.Model):
#     cstatus_name = models.CharField(max_length=50, verbose_name=_("Case Status Name"))
#     created_by = CreatingUserField(related_name = "CaseStatusCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseStatusUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.cstatus_name
#     
#     class Meta:
#         verbose_name = "Case Status"
#         verbose_name_plural = "Case Status"
#         db_table = 'case_status'
# 
# class CaseReviewStatus(models.Model):
#     review_status_name = models.CharField(max_length=50, verbose_name=_("Case Review Status Name"))
#     created_by = CreatingUserField(related_name = "CaseReviewStatusCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseReviewStatusUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.review_status_name
#     
#     class Meta:
#         verbose_name = "Case Review Status"
#         verbose_name_plural = "Case Review Status"
#         db_table = 'case_review_status'
# 
# class CaseListingStatus(models.Model):
#     listing_status_name = models.CharField(max_length=50, verbose_name=_("Case Listing Status Name"))
#     created_by = CreatingUserField(related_name = "CaseListingStatusCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseListingStatusUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.listing_status_name
#     
#     class Meta:
#         verbose_name = "Case Listing Status"
#         verbose_name_plural = "Case Listing Status"
#         db_table = 'case_listing_status'
#         
#         
#         
# 
# 
# class CaseDiagnosis(models.Model):
#     PRIMARY_CHOICES = (
#             (u'1', u'Yes'),
#             (u'0', u'No'),
#         )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History"))
#     dis =  models.ForeignKey(DiseaseMaster,  on_delete=models.CASCADE, verbose_name=_("Case Disease"))
#     is_primary = models.CharField(max_length=1, choices=PRIMARY_CHOICES, verbose_name=_("Is Primary"), default=0)
#     created_by = CreatingUserField(related_name = "CaseDiagnosisCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseDiagnosisUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case.case_title
#     
#     class Meta:
#         verbose_name = "Case Diagnosis"
#         verbose_name_plural = "Case Diagnosis"
#         db_table = 'ccrh_case_diagnosis'
#         
# 
#                         
# class CasePhysicalGeneral(models.Model):
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     hab =  models.ForeignKey(PhysicalGeneralMaster,  on_delete=models.CASCADE, verbose_name=_("General Master "))
#     phygen_value =  models.CharField(max_length=100, verbose_name=_("Physical General Value"))
#     created_by = CreatingUserField(related_name = "CasePhysicalGeneralCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CasePhysicalGeneralUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case.case_title
#     
#     class Meta:
#         verbose_name = "Case Physical General"
#         verbose_name_plural = "Case Physical General"
#         db_table = 'ccrh_case_physical_general'
#         
# class GynaecologicalHistory(models.Model):
#     Leucorrhea_CHOICES = (
#         (u'1', u'quantity'),
#         (u'2', u'color'),
#         (u'3', u'consistency'),
#         (u'4', u'others'),
#     )
#     Character_CHOICES = (
#         (u'1', u'acrid'),
#         (u'2', u'bland'),
#     )
#     Odur_CHOICES = (
#         (u'1', u'odourless'),
#         (u'2', u'offensive'),
#     )
#     Color_CHOICES = (
#         (u'1', u'brightred'),
#         (u'2', u'darkred'),
#         (u'3', u'black'),
#     )
#     Quantity_CHOICES = (
#         (u'1', u'profuse'),
#         (u'2', u'scanty'),
#         (u'3', u'normal'),
#     )
#     HO_HYSTERECTOMY_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     case = models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     menarche_date_age = models.CharField(max_length=15,blank=True,null=True, verbose_name=_("Menarche Date Age"))
#     menst_lmp =  models.CharField(max_length=10, verbose_name=_("Menst Imp"))
#     menst_cycle =  models.CharField(max_length=10, verbose_name=_("Menst Cycle"))
#     menst_duration =  models.CharField(max_length=10, verbose_name=_("Menst Duration"))
#     menst_quantity =  models.CharField(max_length=1,choices=Quantity_CHOICES, verbose_name=_("Menst Quantity"))
#     menst_colour = models.CharField(max_length=1, choices=Color_CHOICES, verbose_name=_("Menst Color"))
#     menst_odur = models.CharField(max_length=1, choices=Odur_CHOICES, verbose_name=_("Menst Odur"))
#     menst_character = models.CharField(max_length=1, choices=Character_CHOICES, verbose_name=_("Menst Character"))
#     menst_complaints_b_d_a_menses = models.TextField(verbose_name=_("Ments Complaints B D A Menses"))
#     menst_leucorrhea = models.CharField(max_length=1, choices=Leucorrhea_CHOICES, verbose_name=_("Menst Leucorrhea"))
#     menst_surgery = models.TextField(verbose_name=_("Ments Surgery"))
#     menopause_date_age = models.CharField(max_length=15,blank=True,null=True, verbose_name=_("MENOPAUSE Date/Age"))
#     ho_hysterectomy = models.CharField(max_length=1,choices=HO_HYSTERECTOMY_CHOICES, verbose_name=_("H/O Hysterectomy"))
#     created_by = CreatingUserField(related_name = "GynaecologicalHistoryCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "GynaecologicalHistoryUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
# 
#     def __str__(self):
#         return self.menst_lmp
#     
#     class Meta:
#         verbose_name = "Gynaecological History "
#         verbose_name_plural = "Gynaecological History"
#         db_table = 'ccrh_case_gynaecological_history'
#         
# class CaseObstrericHistory(models.Model):
#     case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History "))
#     pbh_his_gravida = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Gravida"))
#     pbh_his_para = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Para"))
#     pbh_his_abortion = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Abortion"))
#     pbh_his_stillbirth = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Stillbirth"))
#     pbh_his_living = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy living"))
#     pbh_his_period_of_pregnancy = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Pregnancy"))
#     pbh_his_lactation_history = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Lactation History"))
#     pbh_his_comp_dur_pregnancy = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Comp Dur Pregnancy"))
#     pbh_his_nature_of_labor = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Nature of Labour"))
#     pbh_his_nature_of_delivery = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Nature of Delivery"))
#     pbh_his_nature_of_puerperium = models.TextField(blank=True,null=True,verbose_name=_("Pbh Histroy Nature of Puerperium"))
#     created_by = CreatingUserField(related_name = "CaseObstrericHistoryCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseObstrericHistoryUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case.case_title
#     
#     class Meta:
#         verbose_name = "Case Obstreric History"
#         verbose_name_plural = "Case Obstreric History"
#         db_table = 'ccrh_case_obstreric_history'
#         
# class CaseObstrericChildHistory(models.Model):
#     Child_Alive_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     chd_his_child = models.TextField(verbose_name=_("Lactation History"))
#     chd_his_alive = models.CharField(max_length=1, default=1, choices=Child_Alive_CHOICES, verbose_name=_("Is Alive"))
#     chd_his_causeofdeath =  models.TextField(blank=True,null=True, verbose_name=_("Cause of Death"))
#     chd_his_birthweight =  models.TextField(blank=True,null=True, verbose_name=_("Bright Weight"))
#     created_by = CreatingUserField(related_name = "CaseObstrericChildHistoryCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseObstrericChildHistoryUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.chd_his_child
#     
#     class Meta:
#         verbose_name = "Obstreric Child History  "
#         verbose_name_plural = "Obstreric Child History  "
#         db_table = 'ccrh_case_obstreric_child_history'
#         
# class CasePhysicalFindings(models.Model):
#     Phy_Fin_Order_CHOICES = (
#         (u'1', u'1'),
#         (u'2', u'2'),
#         (u'3', u'3'),
#         (u'4', u'4'),
#         (u'5', u'5'),
#         (u'6', u'6'),
#         (u'7', u'7'),
#     )
#     case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History "))
#     phyfind_order = models.CharField(max_length=1,default=1, choices=Phy_Fin_Order_CHOICES, verbose_name=_("Physical Findings Order"))
#     fin_mas =  models.ForeignKey(PhysicalFindingMaster,  on_delete=models.CASCADE, verbose_name=_("Physical Finding"))
#     phyfind_value = models.TextField(verbose_name=_("Physical Find Value"))
#     created_by = CreatingUserField(related_name = "CasePhysicalFindingsCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CasePhysicalFindingsUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.fin_mas.find_name
#     
#     class Meta:
#         verbose_name = "Physical Findings"
#         verbose_name_plural = "Physical Findings"
#         db_table = 'ccrh_case_phyc_findings'
#         
# class CaseRepertorisation(models.Model):
#     Rep_Analysis_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     case =  models.ForeignKey(CaseHistory, on_delete=models.CASCADE, verbose_name=_("Case History"))
#     rep_document = models.FileField(upload_to='Repertorisation_Upload/',verbose_name=_("Repertorisation  Document"))
#     rep_analysis = models.CharField(max_length=1,default=1, choices=Rep_Analysis_CHOICES, verbose_name=_("Repesntation Analysis"))
#     created_by = CreatingUserField(related_name = "CaseRepertorisationCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseRepertorisationUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.rep_analysis
#     
#     class Meta:
#         verbose_name = "Case Repertorisation "
#         verbose_name_plural = "Case Repertorisation "
#         db_table = 'ccrh_case_repertorisation'
#         
# class CaseMiasamaticAnalysis(models.Model):
#     Mia_Analysis_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History"))
#     mia_analys_mas = models.ForeignKey(MiasamaticAnalysisMaster,  on_delete=models.CASCADE, verbose_name=_("Miasamatic Analysis"))
#     mia_analys_value = models.CharField(max_length=1, choices=Mia_Analysis_CHOICES, verbose_name=_(" Miasamatic Analysis Value"))
#     mia_details = models.TextField(blank=True, null=True, verbose_name=_("Miasamatic Details"))
#     created_by = CreatingUserField(related_name = "CaseMiasamaticAnalysisCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseMiasamaticAnalysisUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.mia_analys_mas.mia_analys_name
#     
#     class Meta:
#         verbose_name = "Case Miasamatic Analysis  "
#         verbose_name_plural = "Case Miasamatic Analysis "
#         db_table = 'ccrh_case_miasamatic_analysis'
#         
# 
# class CaseMedicineManagement(models.Model):
#     Presc_Order_CHOICES = (
#         (u'1', u'1'),
#         (u'2', u'2'),
#         (u'3', u'3'),
#         (u'4', u'4'),
#         (u'5', u'5'),
#         (u'6', u'6'),
#         (u'7', u'7'),
#     )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     prescription_date = models.DateField(verbose_name=_("Prescription Date"))
#     prescription_order = models.CharField(max_length=1,default=1, choices=Presc_Order_CHOICES, verbose_name=_(" Prescription Order"))
#     prescription_oridl_scale = models.TextField(blank=True,null=True,verbose_name=_("Prescription oridl Scale"))
#     outcome_of_prev_presc = models.TextField(blank=True,null=True,verbose_name=_("Outcome of Previous Prescription "))
#     marks_for_improvement = models.TextField(blank=True,null=True,verbose_name=_("Marks for Improvement "))
#     created_by = CreatingUserField(related_name = "CaseMedicineManagementCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseMedicineManagementUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case.case_title
#     
#     class Meta:
#         verbose_name = "Case Medicine Management"
#         verbose_name_plural = "Case Medicine Management "
#         db_table = 'ccrh_case_medicine_management'
#         
# class MedicinePrescriptionMapping(models.Model):
#     medi_mgnt =  models.ForeignKey(CaseMedicineManagement,  on_delete=models.CASCADE, verbose_name=_("Medical Management"))
#     prescription =  models.ForeignKey(MedicineMaster,  on_delete=models.CASCADE, verbose_name=_("Prescription"))
#     potency = models.CharField(max_length=50, verbose_name=_("Potency"))
#     dosage = models.CharField(max_length=50, verbose_name=_("Dosage"))
#     created_by = CreatingUserField(related_name = "MedicinePrescriptionMappingCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "MedicinePrescriptionMappingUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.prescription.med_name
#     
#     class Meta:
#         verbose_name = "Medicine Prescription Mapping"
#         verbose_name_plural = "Medicine Prescription Mapping"
#         db_table = 'ccrh_medicine_prescription_mapping'
#         
# class PrescriptionSymptomMapping(models.Model):
#     medi_pres_map =  models.ForeignKey(MedicinePrescriptionMapping,  on_delete=models.CASCADE, verbose_name=_("Medical Prescription "))
#     symptom =  models.ForeignKey(SymptomsMaster,  on_delete=models.CASCADE, verbose_name=_("Symptoms"))
#     created_by = CreatingUserField(related_name = "PrescriptionSymptomMappingCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PrescriptionSymptomMappingUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.symptom.sym_name
#     
#     class Meta:
#         verbose_name = "Prescription Symptom Mapping"
#         verbose_name_plural = "Prescription Symptom Mapping"
#         db_table = 'ccrh_prescription_symptom_mapping'
# 
# class CaseAddonTherapy(models.Model):
#     Duration_Temper_CHOICES = (
#         (u'1', u'Yes'),
#         (u'2', u'No'),
#     )
#     Addon_Order_CHOICES = (
#         (u'1', u'1'),
#         (u'2', u'2'),
#         (u'3', u'3'),
#         (u'4', u'4'),
#         (u'5', u'5'),
#         (u'6', u'6'),
#         (u'7', u'7'),
#     )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     addon_order = models.CharField(max_length=1, default=1, choices=Addon_Order_CHOICES, verbose_name=_(" Addon Therapy Order"))
#     addon_thrpy_mas = models.ForeignKey(AddonTherapyMaster,  on_delete=models.CASCADE, verbose_name=_("Addon Thearpy "))
#     duration_tamper_homeo = models.CharField(max_length=1,default=1, choices=Duration_Temper_CHOICES, verbose_name=_(" Duration Temper Homeo"))
#     medicine_name = models.CharField(max_length=100,blank=True,null=True,verbose_name=_(" Medicine Name"))
#     medicine_dosage = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("Medicine Dosage"))
#     duration_other_therapy = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("Duration of other therapy(Year/Months/Days)"))
#     duration_after_which_other_therapy = models.CharField(max_length=100,blank=True,null=True,verbose_name=_("Duration after which other therapy (Allopathy/Ayurveda/ Siddha etc) was tapered after homoeopathic treatment"))
#     created_by = CreatingUserField(related_name = "CaseAddonTherapyCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseAddonTherapyUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.addon_thrpy_mas.thrpy_name
#     
#     class Meta:
#         verbose_name = "Case Addon Therapy"
#         verbose_name_plural = "Case Addon Therapy "
#         db_table = 'ccrh_case_addon_therapy '
# 
# class CaseInvestigation(models.Model):
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     investg_mas =  models.ForeignKey(InvestigationsMaster,  on_delete=models.CASCADE, verbose_name=_("Investigation"))
#     investg_value =  models.TextField( blank=True, null=True, verbose_name=_("Investigation Value"))
#     investg_file = models.FileField( blank=True, null=True, verbose_name=_("Investigation File"))
#     created_by = CreatingUserField(related_name = "CaseInvestigationCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseInvestigationUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case.case_title + ' - ' +self.investg_mas.investg_name
#     
#     class Meta:
#         verbose_name = "Case Investigation"
#         verbose_name_plural = "Case Investigation"
#         db_table = 'ccrh_case_investigation'
# 
# class CaseStatusHistory(models.Model):
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     case_status  =  models.ForeignKey(CaseStatus,  on_delete=models.CASCADE, verbose_name=_("Case Status"))
#     case_remarks =  models.TextField( verbose_name=_("Case Remarks"))
#     created_by = CreatingUserField(related_name = "CaseStatusHistoryCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseStatusHistoryUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case_status.cstatus_name
#     
#     class Meta:
#         verbose_name = "Case Status History"
#         verbose_name_plural = "Case Status History"
#         db_table = 'ccrh_case_status_history'
#         
# class CaseReviewStatusHistory(models.Model):
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     case_review_status  =  models.ForeignKey(CaseReviewStatus,  on_delete=models.CASCADE, verbose_name=_("Case Review Status"))
#     case_review_remarks =  models.TextField( verbose_name=_("Case Review Remarks"))
#     created_by = CreatingUserField(related_name = "CaseReviewStatusHistoryCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseReviewStatusHistoryUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.case_review_status.review_status_name
#     
#     class Meta:
#         verbose_name = "Case Review Status History"
#         verbose_name_plural = "Case Review Status History"
#         db_table = 'ccrh_case_review_status_history'
#         
#         
# class CaseChecklistMapping(models.Model):
#     Checklist_CHOICES =  (
#         (u'1', u'Yes'),
#         (u'0', u'No'),
#     )
#     case =  models.ForeignKey(CaseHistory,  on_delete=models.CASCADE, verbose_name=_("Case History "))
#     checklist  =  models.ForeignKey(CaseCheckListMaster,  on_delete=models.CASCADE, verbose_name=_("Case CheckList"))
#     checklist_value =  models.CharField(max_length=1, choices=Checklist_CHOICES, verbose_name=_("Checklist Value"))
#     created_by = CreatingUserField(related_name = "CaseChecklistMappingCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "CaseChecklistMappingUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
# 
#     def __str__(self):
#         return self.checklist.checklist_name
#     
#     class Meta:
#         verbose_name = "Case Checklist Mapping"
#         verbose_name_plural = "Case Checklist Mapping"
#         db_table = 'ccrh_case_checklist_mapping'
#         
# #case Investigation mapping table starts here
# class InvestigationcategoryMapping(models.Model):
#     investg =  models.ForeignKey(CaseInvestigation,  on_delete=models.CASCADE, verbose_name=_("Investigation "))
#     investg_cat  =  models.ForeignKey(InvestigationCategoryMaster,  on_delete=models.CASCADE, verbose_name=_("Investigation Category Master"))
#     investg_cat_value =  models.TextField( blank=True, null=True, verbose_name=_("Investigation Category Value"))
#     created_by = CreatingUserField(related_name = "InvestigationcategoryMappingCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "InvestigationcategoryMappingUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.investg_cat.investg_cat_name
#     
#     class Meta:
#         verbose_name = "Investigation category Mapping"
#         verbose_name_plural = "Investigation category Mapping"
#         db_table = 'ccrh_case_investigation_category_mapping'

