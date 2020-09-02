from djongo import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from audit_log.models.fields import CreatingUserField, LastUserField
from django.db.models.deletion import CASCADE
from random import choices
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator
from ckeditor.fields import RichTextField
from treenode.models import TreeNodeModel

'''FINALIZED MODELS STARTS'''

#State Model Starts here
class State(models.Model):
    _id = models.ObjectIdField()
    COUNTRY_CHOICES = (
        (u'1', u'INDIA'),
    )
    state_name = models.CharField(max_length=100, verbose_name=_("State Name"))
    country_id = models.CharField(max_length=1, default=1, choices=COUNTRY_CHOICES, verbose_name=_("Country Name"))

    def __str__(self):
        return self.state_name
    
    class Meta:
        verbose_name = "State"
        verbose_name_plural = "State"
        db_table = 'ccrh_state_master'
#State Model Ends here

#City Model Starts here
class City(models.Model):
    _id = models.ObjectIdField()
    state =  models.ForeignKey(State,  on_delete=models.CASCADE, verbose_name=_("State Name"))
    city_name = models.CharField(max_length=100, verbose_name=_("City Name"))

    def __str__(self):
        return self.city_name
    
    class Meta:
        verbose_name = "City"
        verbose_name_plural = "City"
        db_table = 'ccrh_city_master'
#City Model Ends here
 
#Clinical Setting Model Starts here
class ClinicalSetting(models.Model):
    _id = models.ObjectIdField()
    cs_name = models.CharField(max_length=100, verbose_name=_("Clinical Setting Name"))

    def __str__(self):
        return self.cs_name
    
    class Meta:
        verbose_name = "Clinical Setting"
        verbose_name_plural = "Clinical Setting"
        db_table = 'ccrh_pract_clinical_setting_master'
#Clinical Setting Model Ends here

#Hospital Master Model Starts Here
class HospitalMaster(models.Model):
    _id = models.ObjectIdField()
    hospital_name = models.CharField(max_length=250, verbose_name=_("Hospital Name"))
    hospital_type = models.ForeignKey(ClinicalSetting, on_delete=models.CASCADE, verbose_name=_("Hospital Type"))
    address_1 =  models.TextField(blank=True, null=True,verbose_name=_("Address 1"))
    address_2 =  models.TextField(blank=True, null=True,verbose_name=_("Address 2"))
    city =  models.ForeignKey(City, on_delete=models.CASCADE, verbose_name=_("City"))
    state =  models.ForeignKey(State, on_delete=models.CASCADE, verbose_name=_("State"))
    pincode = models.BigIntegerField(blank=True, null=True,  verbose_name=_("Pin Code"))
    permitted_seats =  models.TextField(blank=True,null=True,verbose_name=_("Permitted Seats"))
    master_flag = models.BooleanField(default=False, verbose_name=_("Master Flag"))
    
    def __str__(self):
        return self.hospital_name
    
    class Meta:
        verbose_name = "Hospital Master "
        verbose_name_plural = "Hospital Master"
        db_table = 'ccrh_hospital_master'
#Hospital Master Model Ends Here  
 
#Symptoms Master Model Starts Here    
class SymptomsMaster(models.Model):
    _id = models.ObjectIdField()
    sym_name = models.TextField(verbose_name=_("Symptoms Name"))
    sym_desc = models.TextField(blank=True, null=True, verbose_name=_("Symptoms Description"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "SymptomsMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "SymptomsMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.sym_name
    
    class Meta:
        verbose_name = "Symptoms Master "
        verbose_name_plural = "Symptoms Master"
        db_table = 'ccrh_symptoms_master'
#Symptoms Master Model Ends Here
        
#Disease Master Model Starts Here
class DiseaseMaster(TreeNodeModel):
    # the field used to display the model instance
    # default value 'pk'
    treenode_display_field = 'dis_name'
    dis_name = models.CharField(max_length=250, verbose_name=_("Category / Sub-Category / Disease Name"))
    icd_range = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("ICD Code Range"))
    dis_icd_code = models.CharField(max_length=50,blank=True, null=True, verbose_name=_("ICD Code"))
    dis_desc = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    dis_mapped = models.TextField(blank=True, null=True, verbose_name=_("Cross Referencing Disease Code"), help_text=_("Kindly enter comma separated ICD Code without any other special chars like spaces Example - M01.3,G01,M90.2,J17.0,N16.0"))
    
    def __str__(self):
        return self.dis_name
    
    class Meta(TreeNodeModel.Meta):
        verbose_name = 'Disease Master'
        verbose_name_plural = 'Disease Master'
        db_table = 'ccrh_disease_master'
        indexes = [
            models.Index(fields=['dis_name', 'dis_icd_code'])
        ]
#Disease Master Model Ends Here
      
#Diet Master Starts Here
class DietsMaster(models.Model):
    _id = models.ObjectIdField()
    diet_name = models.CharField(max_length=100, verbose_name=_("Diet Name"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "DietsMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "DietsMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.diet_name

    class Meta:
        verbose_name = "Diet Master"
        verbose_name_plural = "Diet Master"
        db_table = 'ccrh_diets_master'
#Diet Master Ends Here

#Habits Master Starts Here
class HabitsMaster(models.Model):
    _id = models.ObjectIdField()
    hab_name = models.CharField(max_length=100, verbose_name=_("Habit Name"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "HabitsMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "HabitsMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.hab_name

    class Meta:
        verbose_name = "Habit Master "
        verbose_name_plural = "Habit Master"
        db_table = 'ccrh_habits_master'
#Habit Master Ends Here

#Mental General  Master Starts Here
class MentalGeneralMaster(models.Model):
    _id = models.ObjectIdField()
    mental_general_val = models.CharField(max_length=250, verbose_name=_("Mental General Value"))
    mental_desc = models.TextField(blank=True, null=True, verbose_name=_("Mental General Description"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "MentalGeneralMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "MentalGeneralMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
     
    def __str__(self):
        return self.mental_general_val
     
    class Meta:
        verbose_name = "Mental General Master"
        verbose_name_plural = "Mental General Master"
        db_table = 'ccrh_mental_general_master'
#Mental General Master Ends Here

#Email Template Model Starts Here        
class EmailTemplate(models.Model):
    _id = models.ObjectIdField()
    email_code = models.CharField(max_length=10, verbose_name=_("Email Code"))
    email_subject = models.TextField(verbose_name=_("Email Subject"))
    email_body = RichTextField(verbose_name=_("Email Body"), help_text=_("Note : Do not change the text inside curly braces {}"))
    sent_to = models.CharField(blank=True, null=True, max_length=200, verbose_name=_("Send To"))
    trigger_point = models.TextField(blank=True, null=True, verbose_name=_("Trigger Point"))
    created_by = CreatingUserField(related_name = "EmailTemplateCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "EmailTemplateUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.email_code
    
    class Meta:
        verbose_name_plural = "Email Template"
        db_table = 'ccrh_email_template'
#Email Template Model Ends Here

#SMS Template Model Starts here
class SmsTemplate(models.Model):
    _id = models.ObjectIdField()
    sms_code = models.CharField(max_length=10, verbose_name=_("SMS Code"))
    sms_text = models.TextField(verbose_name=_("SMS Text"), help_text=_("Note : Do not change the text inside curly braces {}"))
    trigger_point = models.TextField(blank=True, null=True, verbose_name=_("Trigger Point"))
    sent_to = models.CharField(blank=True, null=True, max_length=200, verbose_name=_("Send To"))
    created_by = CreatingUserField(related_name = "SmsTemplateCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "SmsTemplateUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.sms_code
    
    class Meta:
        verbose_name_plural = "SMS Template"
        db_table = 'ccrh_sms_template'
#SMS Template Model Ends here
                
#Case Category Model Starts here.
class CaseCategory(models.Model):
    _id = models.ObjectIdField()
    category_name = models.CharField(max_length=50, verbose_name=_("Category Name"))
    icd_code = models.CharField(max_length=50, verbose_name=_("ICD Code"), help_text=_("EX: A00-B99"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "CaseCategoryCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "CaseCategoryUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = "Case Category"
        verbose_name_plural = "Case Category"
        db_table = 'case_category'
#Case Category Model Ends here

#Case CheckList Master Model Ends here
class CaseCheckListMaster(models.Model):
    _id = models.ObjectIdField()
    checklist_name = models.CharField(max_length=150, verbose_name=_("CheckList Name"))
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "CaseCheckListMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "CaseCheckListMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.checklist_name
    
    class Meta:
        verbose_name = "Case CheckList Master"
        verbose_name_plural = "Case CheckList Master"
        db_table = 'case_checklist_master'
#Case CheckList Master Model Ends here
      
#Medicine Master Model Starts here
#Medicine Type Model using Medicine Master as Embedded Field in Starts here    
class MedicineType(models.Model):
    mother_tincture = models.BooleanField(default=False, verbose_name=_("Mother Tincture"))
    ointment = models.BooleanField(default=False, verbose_name=_("Ointment"))
    biochemic = models.BooleanField(default=False, verbose_name=_("Biochemic"))
    oil = models.BooleanField(default=False, verbose_name=_("Oil"))
    ear_drop = models.BooleanField(default=False, verbose_name=_("Rar Drop"))
    eye_drop = models.BooleanField(default=False, verbose_name=_("Ear Drop"))

    def __str__(self):
        return str(self.mother_tincture)
    
    class Meta:
        abstract = True
#Medicine Type Model using Medicine Master as Embedded Field in Ends here    

#Potencies Model using Medicine Master as Embedded Field in Starts here      
class Potencies(models.Model):
    mother_tincture = models.BooleanField(default=False, verbose_name=_("Mother Tincture"))
    potency_3x =  models.BooleanField(default=False, verbose_name=_("Potency 3X"))
    potency_6x =  models.BooleanField(default=False, verbose_name=_("Potency 6X"))
    potency_6 =  models.BooleanField(default=False, verbose_name=_("Potency 6"))
    potency_30 = models.BooleanField(default=False, verbose_name=_("Potency 30"))
    potency_200 = models.BooleanField(default=False, verbose_name=_("Potency 200"))
    potency_1m = models.BooleanField(default=False, verbose_name=_("Potency 1M"))
    potency_10m = models.BooleanField(default=False, verbose_name=_("Potency 10M"))
    potency_lm = models.BooleanField(default=False, verbose_name=_("Potency LM"))

    def __str__(self):
        return str(self.mother_tincture)
    
    class Meta:
        abstract = True
#Potencies Model using Medicine Master as Embedded Field in Ends here      

#Sources Model Starts here    
class Sources(models.Model):
    plant = models.BooleanField(default=False, verbose_name=_("Plant"))
    chemical =  models.BooleanField(default=False, verbose_name=_("Chemical"))
    metal_non_metal =  models.BooleanField(default=False, verbose_name=_("Metal Non-Metal"))
    imponderabilia =  models.BooleanField(default=False, verbose_name=_("Imponderabilia"))
    minerals_ore_oxide = models.BooleanField(default=False, verbose_name=_("Minerals Ore-Oxide"))
    zoological = models.BooleanField(default=False, verbose_name=_("Zoological"))
    nosode = models.BooleanField(default=False, verbose_name=_("Nosode"))
    sarcode = models.BooleanField(default=False, verbose_name=_("Sarcode"))

    def __str__(self):
        return str(self.plant)
    
    class Meta:
        abstract = True
#Sources Model Ends here

class MedicineMaster(models.Model):
    _id = models.ObjectIdField()
    med_name = models.CharField(max_length=100, verbose_name=_("Medicine Name"))
    medicine_type = models.EmbeddedField(
        model_container=MedicineType,
        null=True
    )
    potencies = models.EmbeddedField(
        model_container=Potencies,
        null=True
    )
    internal_application  = models.TextField(blank=True, null=True, verbose_name=_("Internal Application"))
    external_application = models.TextField(blank=True, null=True, verbose_name=_("External Application"))
    sources = models.EmbeddedField(
        model_container=Sources,
        null=True
    )
    master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
    created_by = CreatingUserField(related_name = "MedicineMasterCreatedBy")
    created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated_by = LastUserField(related_name = "MedicineMasterUpdatedBy")
    updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __str__(self):
        return self.med_name
    
    class Meta:
        verbose_name = "Medicine Master "
        verbose_name_plural = "Medicine Master"
        db_table = 'ccrh_medicine_master'
#Medicine Master Model Ends here
'''FINALIZED MODELS ENDS'''



# #Addon Therapy Master Starts Here
# class AddonTherapyMaster(models.Model):
#     _id = models.ObjectIdField()
#     thrpy_name = models.CharField(max_length=100, verbose_name=_("Therapy Name"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "AddonTherapyMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "AddonTherapyMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.thrpy_name
#     
#     class Meta:
#         verbose_name = "Addon Therapy Master"
#         verbose_name_plural = "Addon Therapy Master"
#         db_table = 'ccrh_addon_therapy_master'
# #Addon Therapy Master Ends Here


# #Family Relation Master Starts Here
# class FamilyRelationMaster(models.Model):
#     _id = models.ObjectIdField()
#     relation = models.CharField(max_length=150, verbose_name=_("Relation"))
# 
#     def __str__(self):
#         return self.relation
# 
#     class Meta:
#         verbose_name = "Family Relation Master"
#         verbose_name_plural = "Family Relation Master"
#         db_table = 'ccrh_family_relation_master'
# #Family Relation Master Ends Here

# #Physical Finding Type Model Starts Here    
# class PhysicalFindingType(models.Model):
#     _id = models.ObjectIdField()
#     find_type = models.CharField(max_length=100, verbose_name=_("Physical Find Type"), unique=True)
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PhysicalFindingTypeCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PhysicalFindingTypeUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.find_type
#     
#     class Meta:
#         verbose_name = "Physical Finding Type"
#         verbose_name_plural = "Physical Finding Type"
#         db_table = 'ccrh_phy_finding_type'
# #Physical Finding Type Model Ends Here    
# 
# #Physical Finding Master Model Starts Here    
# class PhysicalFindingMaster(models.Model):
#     _id = models.ObjectIdField()
#     fin_type = models.ForeignKey(PhysicalFindingType,  on_delete=models.CASCADE, verbose_name=_("Physical Find Type"))
#     find_name = models.CharField(max_length=100, verbose_name=_("Physical Find Name"))
#     measurement = models.CharField(max_length=100, verbose_name=_("Measurement"), unique=True)
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PhysicalFindingMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PhysicalFindingMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.find_name
#     
#     class Meta:
#         verbose_name = "Physical Finding Master"
#         verbose_name_plural = "Physical Finding Master"
#         db_table = 'ccrh_phy_finding_master'
# #Physical Finding Master Model Ends Here 


        

        
        
# #Investigation Model Starts Here
# class InvestigationsMaster(models.Model):
#     _id = models.ObjectIdField()
#     investg_name = models.CharField(max_length=150, verbose_name=_("Investigation Name"), unique=True)
#     investg_desc = models.TextField( verbose_name="Investigation Description")
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "InvestigationsMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "InvestigationsMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.investg_name
#     
#     class Meta:
#         verbose_name = "Investigation Master "
#         verbose_name_plural = "Investigation Master"
#         db_table = 'ccrh_investigation_master'
# #Investigation Model Ends Here


# #Physical General Type Model Starts Here
# class PhysicalGeneralType(models.Model):
#     _id = models.ObjectIdField()
#     gen_type_name = models.CharField(max_length=100, verbose_name=_("General Type Name"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PhysicalGeneralTypeCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PhysicalGeneralTypeUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
# 
#     def __str__(self):
#         return self.gen_type_name 
#     
#     class Meta:
#         verbose_name = "Physical General Type "
#         verbose_name_plural = "Physical General Type"
#         db_table = 'ccrh_phy_general_type'
# #Physical General Type Model Ends Here

        
# #Physical General Master Model Starts Here
# class PhysicalGeneralMaster(models.Model):
#     Genearl_Type_CHOICES = (
#         (u'1', u'Dropdown'),
#         (u'2', u'TEXT'),
#     )
#     _id = models.ObjectIdField()
#     gen_type = models.ForeignKey(PhysicalGeneralType,  on_delete=models.CASCADE, verbose_name=_("General Type"))
#     gen_name = models.CharField(max_length=100, verbose_name=_("General Name"))
#     gen_value_type = models.CharField(max_length=1,choices=Genearl_Type_CHOICES, verbose_name=_("General Value Type"))
#     dropdown_values = models.TextField(verbose_name=_("DropDown Values"), blank=True, null=True, help_text=_("Note : Please fill the box in following format - ['Obese', 'Thin', 'Emaciated'] if General Value Type field is marked as Dropdown."))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PhysicalGeneralMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PhysicalGeneralMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.gen_name
#     
#     class Meta:
#         verbose_name = "Physical General Master"
#         verbose_name_plural = "Physical General Master"
#         db_table = 'ccrh_phy_general_master'
# #Physical General Master Model Ends Here

        
# #Past History Model Starts Here
# class PastHistoryType(models.Model):
#     _id = models.ObjectIdField()
#     his_type_name = models.CharField(max_length=100, verbose_name=_("History Type Name"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PastHistoryTypeCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PastHistoryTypeUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.his_type_name
#     
#     class Meta:
#         verbose_name = "Past History Type "
#         verbose_name_plural = "Past History Type"
#         db_table = 'ccrh_past_history_type'
# #Past History Model Ends Here

        
# #Past History Master Model Starts Here
# class PastHistoryMaster(models.Model):
#     _id = models.ObjectIdField()
#     his_type = models.ForeignKey(PastHistoryType,  on_delete=models.CASCADE, verbose_name=_("History Type"))
#     his_name = models.CharField(max_length=100, verbose_name=_("History Name"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "PastHistoryMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "PastHistoryMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
# 
#     def __str__(self):
#         return self.his_name
#     
#     class Meta:
#         verbose_name = "Past History Master"
#         verbose_name_plural = "Past History Master"
#         db_table = 'ccrh_past_hisory_master'
# #Past History Master Model Ends Here
# 
# 
# #Miasamatic Analysis Master Model Starts Here    
# class MiasamaticAnalysisMaster(models.Model):
#     _id = models.ObjectIdField()
#     mia_analys_name = models.CharField(max_length=100, verbose_name=_("Miasamatic Analysis Name"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "MiasamaticAnalysisMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "MiasamaticAnalysisMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
# 
#     def __str__(self):
#         return self.mia_analys_name
#     
#     class Meta:
#         verbose_name = "Miasamatic Analysis Master"
#         verbose_name_plural = "Miasamatic Analysis Master"
#         db_table = 'ccrh_miasamatic_analysis_master'
# #Miasamatic Analysis Master Model Ends Here    
# 
#            
# #Investigation Category Master Model Starts Here
# class InvestigationCategoryMaster(models.Model):
#     _id = models.ObjectIdField()
#     investg_cat_name = models.CharField(max_length=150, verbose_name=_("Investigation Category Name"))
#     investg_cat_unit = models.CharField(max_length=150,blank=True,null=True, verbose_name=_("Investigation Category Unit"))
#     investg_mas = models.ForeignKey(InvestigationsMaster,  on_delete=models.CASCADE, verbose_name=_("Investigation Master"))
#     master_flag = models.BooleanField(default=True, verbose_name=_("Master Flag"))
#     created_by = CreatingUserField(related_name = "InvestigationCategoryMasterCreatedBy")
#     created_date = models.DateTimeField(auto_now_add=True,auto_now=False)
#     updated_by = LastUserField(related_name = "InvestigationCategoryMasterUpdatedBy")
#     updated_date = models.DateTimeField(auto_now_add=False, auto_now=True)
#     
#     def __str__(self):
#         return self.investg_cat_name
#     
#     class Meta:
#         verbose_name = "Investigation Category Master"
#         verbose_name_plural = "Investigation Category Master"
#         db_table = 'ccrh_investigation_category_master'
# #Investigation Category Master Model Ends Here