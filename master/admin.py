"""
Project    : "CCRH"
module     : master/admin
created    : 03/03/2020
Author     : Manish Kumar
"""

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from master.models import (State, DietsMaster, EmailTemplate,SmsTemplate, ClinicalSetting,
                           HospitalMaster,CaseCategory,CaseCheckListMaster,
                           City,HabitsMaster, DiseaseMaster, SymptomsMaster,
                           MentalGeneralMaster,MedicineMaster
                           )
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, IntegerWidget
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.formats import base_formats
from django.forms import forms, ModelForm, Select
from import_export import resources, fields
from treenode.admin import TreeNodeModelAdmin
from treenode.forms import TreeNodeForm


'''FINALIZED ADMIN STARTS'''

#State Admin Starts Here
class StateResource(resources.ModelResource):
    state_name = fields.Field(column_name=_('State Name'), attribute='state_name')
    country_id = fields.Field(column_name=_('Country Id'), attribute='country_id',)
    
    class Meta:
        model = State
        fields = ('state_name','country_id', )
        import_id_fields = fields
        export_order = fields
    
class StateAdmin(ImportExportModelAdmin):
    resource_class = StateResource
    list_display = ('state_name','country_id', )
    search_fields = ('state_name',)
#State Admin Ends Here

#City Admin Starts Here
class CityResource(resources.ModelResource):
    city_name = fields.Field(column_name=_('City Name'), attribute='city_name')
    state = fields.Field(column_name=_('State Name'), attribute='state', widget=ForeignKeyWidget(State, 'state_name'))
    
    class Meta:
        model = City
        fields = ('city_name', 'state',)
        import_id_fields = fields
        export_order = fields
    
class CityAdmin(ImportExportModelAdmin):
    resource_class = CityResource
    list_display = ('city_name','state', )
    search_fields = ('city_name','state__state_name',)
    list_filter = ('state',)
#City Admin End Here

#Clinical Setting Admin Starts Here
class ClinicalsettingResource(resources.ModelResource):
    cs_name = fields.Field(column_name=_('Clinical Setting Name'), attribute='cs_name')
    
    class Meta:
        model = ClinicalSetting
        fields = ('cs_name',)
        import_id_fields = fields
        export_order = fields
    
class ClinicalsettingAdmin(ImportExportModelAdmin):
    resource_class = ClinicalsettingResource
    list_display = ('cs_name', )
    search_fields = ('cs_name',)
    list_filter = ('cs_name',)
#Clinical Setting Admin Ends Here

#Hospital Master  Admin starts here
class HospitalMasterResource(resources.ModelResource):
    hospital_name = fields.Field(column_name=_('Hospital Name'), attribute='hospital_name')
    hospital_type = fields.Field(column_name=_('Hospital Type'), attribute='hospital_type', widget=ForeignKeyWidget(ClinicalSetting, 'cs_name'))
    address_1 = fields.Field(column_name=_('Address 1'), attribute='address_1')
    address_2 = fields.Field(column_name=_('Address 2'), attribute='address_2')
    city = fields.Field(column_name=_('City Name'), attribute='city', widget=ForeignKeyWidget(City, 'city_name'))
    state = fields.Field(column_name=_('State Name'), attribute='state', widget=ForeignKeyWidget(State, 'state_name'))
    pincode = fields.Field(column_name=_('Pincode'), attribute='pincode')
    permitted_seats=fields.Field(column_name=_('Permitted Seats'), attribute='permitted_seats')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
    
    class Meta:
        model = HospitalMaster
        fields = ('hospital_name','hospital_type','address_1','address_2','city','state','pincode','permitted_seats',)
        import_id_fields = fields
        export_order = fields
    
class HospitalMasterAdmin(ImportExportModelAdmin):
    resource_class = HospitalMasterResource
    list_display =  ('hospital_name','hospital_type','address_1','address_2','city','state','pincode','permitted_seats',)
    search_fields = ('hospital_name','hospital_type',)
#Hospital Master  Admin Ends Here   

#Symptoms Admin Starts Here
class SymptomsMasterResource(resources.ModelResource):
    sym_name = fields.Field(column_name=_('Symptoms Name'), attribute='sym_name')
    sym_desc = fields.Field(column_name=_('Symptoms Description'), attribute='sym_desc')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
    
    class Meta:
        model = SymptomsMaster
        fields = ('sym_name','sym_desc','master_flag',)
        import_id_fields = fields
        export_order = fields
    
class SymptomsMasterAdmin(ImportExportModelAdmin):
    resource_class = SymptomsMasterResource
    list_display =  ('sym_name','sym_desc','master_flag',)
    search_fields = ('sym_name','sym_desc','master_flag',)
    list_filter = ('master_flag',)
#Symptoms Admin Ends Here

#Disease Admin Starts Here
# class DiseaseMasterAdmin(TreeNodeModelAdmin):
#     list_display = ('dis_name','icd_range','dis_icd_code')
#     # set the changelist display mode: 'accordion', 'breadcrumbs' or 'indentation' (default)
#     # when changelist results are filtered by a querystring,
#     # 'breadcrumbs' mode will be used (to preserve data display integrity)
#     treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_ACCORDION
#     # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_BREADCRUMBS
#     # treenode_display_mode = TreeNodeModelAdmin.TREENODE_DISPLAY_MODE_INDENTATION
# 
#     # use TreeNodeForm to automatically exclude invalid parent choices
#     form = TreeNodeForm
    
class DiseaseMasterResource(resources.ModelResource):
    dis_name = fields.Field(column_name=_("Category / Sub-Category / Disease Name"), attribute='dis_name')
    icd_range = fields.Field(column_name=_("ICD Code Range"), attribute='icd_range')
    dis_icd_code = fields.Field(column_name=_("ICD Code"), attribute='dis_icd_code')
    dis_desc = fields.Field(column_name=_("Description"), attribute='dis_desc')
    dis_mapped = fields.Field(column_name=_("Cross Referencing Disease Code"), attribute='dis_mapped')

    class Meta:
        model= DiseaseMaster
        fields= ('dis_name','icd_range','dis_icd_code','dis_desc','dis_mapped')
        import_id_fields = fields
        export_order = fields

class DiseaseMasterAdmin(ImportExportModelAdmin):
    resource_class= DiseaseMasterResource
    list_display = ('dis_name','icd_range','dis_icd_code','dis_desc','dis_mapped')
    search_fields = ('dis_name','icd_range','dis_icd_code','dis_desc','dis_mapped')
    list_filter = ('dis_name','icd_range','dis_icd_code')
#Disease Admin Ends Here

#Diet Master Admin Starts Here
class DietsMasterResource(resources.ModelResource):
    diet_name = fields.Field(column_name=_("Diet Name"), attribute='diet_name')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')

    class Meta:
        model= DietsMaster
        fields= ('diet_name','master_flag')
        import_id_fields = fields
        export_order = fields

class DietsMasterAdmin(ImportExportModelAdmin):
    resource_class= DietsMasterResource
    list_display = ('diet_name', 'master_flag',)
    search_fields = ('diet_name','master_flag',)
    list_filter = ('diet_name',)
#Diet Master Admin Ends Here

#Habit Master Admin Starts Here
class HabitsMasterResource(resources.ModelResource):
    hab_name = fields.Field(column_name=_('Habit Name'), attribute='hab_name')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')

    class Meta:
        model = HabitsMaster
        fields = ('hab_name','master_flag',)
        import_id_fields = fields
        export_order = fields

class HabitsMasterAdmin(ImportExportModelAdmin):
    resource_class = HabitsMasterResource
    list_display =  ('hab_name','master_flag',)
    search_fields = ('hab_name','master_flag',)
    list_filter = ('hab_name',)
#Habit Master Admin Ends Here

#Mental General Master Admin Starts Here
class MentalGeneralMasterResource(resources.ModelResource):
    mental_general_val = fields.Field(column_name=_('Mental General Value'), attribute='mental_general_val')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
     
    class Meta:
        model = MentalGeneralMaster
        fields = ('mental_general_val','master_flag',)
        import_id_fields = fields
        export_order = fields
     
class MentalGeneralMasterAdmin(ImportExportModelAdmin):
    resource_class = MentalGeneralMasterResource
    list_display =  ('mental_general_val','master_flag',)
    search_fields = ('mental_general_val',)
#Mental General Master  Admin Ends Here 

#Email Template Admin Starts Here
class EmailTemplateResource(resources.ModelResource):
    email_code = fields.Field(column_name='Email Code', attribute='email_code')
    email_subject = fields.Field(column_name='Email Subject', attribute='email_subject')
    sent_to = fields.Field(column_name='Send To', attribute='sent_to')
    trigger_point = fields.Field(column_name='Trigger Point', attribute='trigger_point')
    
    class Meta:
        model = EmailTemplate
        fields = ('sent_to','trigger_point','email_code','email_subject','email_body')
        export_order = fields

class EmailTemplateAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = EmailTemplateResource
    list_display = ('email_code','email_subject','sent_to','trigger_point')
    search_fields = ('email_code','email_subject','sent_to','trigger_point')
    fields = ('email_code','sent_to','trigger_point','email_subject','email_body')
    readonly_fields=('email_code',)
    
    def has_delete_permission(self, request, obj=None):
        return False
#Email Template Admin Ends Here

#SMS Template Admin Starts Here
class SMSTemplateResource(resources.ModelResource):
    sms_code = fields.Field(column_name='SMS Code', attribute='sms_code')
    sms_text = fields.Field(column_name='SMS Text', attribute='sms_text')
    sent_to = fields.Field(column_name='Send To', attribute='sent_to')
    trigger_point = fields.Field(column_name='Trigger Point', attribute='trigger_point')
    
    class Meta:
        model = SmsTemplate
        fields = ('sent_to','trigger_point','sms_code','sms_text')
        export_order = fields


class SmsTemplateAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = SMSTemplateResource
    list_display = ('sms_code','sms_text','sent_to','trigger_point')
    search_fields = ('sms_code','sms_text','sent_to','trigger_point')
    fields = ('sms_code','sent_to','trigger_point','sms_text')
    readonly_fields=('sms_code',)
    
    def has_delete_permission(self, request, obj=None):
        return False
#SMS Template Admin Ends Here

#CaseCategory admin starts here
class CaseCategoryResource(resources.ModelResource):
    category_name = fields.Field(column_name=_('Category Name'), attribute='category_name')
    icd_code = fields.Field(column_name=_('ICD Code'), attribute='icd_code')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
     
    class Meta:
        model = CaseCategory
        fields = ('category_name','icd_code','master_flag',)
        import_id_fields = fields
        export_order = fields
     
     
class CaseCategoryAdmin(ImportExportModelAdmin):
    resource_class = CaseCategoryResource
    list_display = ('category_name','icd_code','master_flag',)
    search_fields = ('category_name','icd_code','master_flag',)
    list_filter = ('category_name','icd_code','master_flag',)
#CaseCategory Admin Ends Here

#CaseCheckListMaster admin starts here
class CaseCheckListMasterResource(resources.ModelResource):
    checklist_name = fields.Field(column_name=_('CheckList Name'), attribute='checklist_name')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
     
    class Meta:
        model = CaseCheckListMaster
        fields = ('checklist_name','master_flag',)
        import_id_fields = fields
        export_order = fields
     
class CaseCheckListMasterAdmin(ImportExportModelAdmin):
    resource_class = CaseCheckListMasterResource
    list_display = ('checklist_name','master_flag',)
    search_fields = ('checklist_name','master_flag',)
    list_filter = ('checklist_name','master_flag',)
#CaseCheckListMaster Admin Ends Here
   
#Medicine Master Admin Starts Here
class MedicineMasterResource(resources.ModelResource):
    med_name = fields.Field(column_name=_('Medicine Name'), attribute='med_name')
    master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
     
    class Meta:
        model = MedicineMaster
        fields = ('med_name','medicine_type','potencies', 'internal_application', 
                  'external_application','sources','master_flag',)
        import_id_fields = fields
        export_order = fields
     
class MedicineMasterAdmin(ImportExportModelAdmin):
    resource_class = MedicineMasterResource
    list_display =  ('med_name','medicine_type','potencies', 'internal_application', 
                  'external_application','sources','master_flag',)
    search_fields = ('med_name','internal_application','external_application','master_flag',)
    list_filter = ('med_name', 'external_application','external_application','master_flag')
#Medicine Master Admin Ends Here    
'''FINALIZED ADMIN STARTS'''




# #Addon Therapy Admin Starts Here
# class AddonTherapyMasterResource(resources.ModelResource):
#     thrpy_name = fields.Field(column_name=_('Therapy Name'), attribute='thrpy_name')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = AddonTherapyMaster
#         fields = ('thrpy_name','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class AddonTherapyMasterAdmin(ImportExportModelAdmin):
#     resource_class = AddonTherapyMasterResource
#     list_display =  ('thrpy_name','master_flag',)
#     search_fields = ('thrpy_name','master_flag',)
#     list_filter = ('thrpy_name',)
# #Addon Therapy Admin Ends Here 

# #Family Relation Master Admin Starts Here
# class FamilyRelationMasterResource(resources.ModelResource):
#     relation =fields.Field(column_name=_("Realtion"), attribute='relation')
# 
#     class Meta:
#         model = FamilyRelationMaster
#         fields = ('relation',)
#         import_id_fields = fields
#         export_order = fields
# 
# class FamilyRelationMasterAdmin(ImportExportModelAdmin):
#     resource_class = FamilyRelationMasterResource
#     list_display =  ('relation',)
#     search_fields = ('relation',)
# #Family Relation Master Admin Ends Here


# #Physical Finding Type Admin Starts Here
# class PhysicalFindingTypeResource(resources.ModelResource):
#     find_type = fields.Field(column_name=_('Physical Find Type'), attribute='find_type')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = PhysicalFindingType
#         fields = ('find_type','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PhysicalFindingTypeAdmin(ImportExportModelAdmin):
#     resource_class = PhysicalFindingTypeResource
#     list_display =  ('find_type','master_flag',)
#     search_fields = ('find_type','master_flag',)
#     list_filter = ('find_type',)
# #Physical Finding Type Admin Ends Here   
#   
# #Physical Finding Master Admin Starts Here
# class PhysicalFindingMasterResource(resources.ModelResource):
#     fin_type = fields.Field(column_name=_('Physical Find Type'), attribute='fin_type', widget=ForeignKeyWidget(PhysicalFindingType, 'find_type'))
#     find_name = fields.Field(column_name=_('Physical Find Name'), attribute='find_name')
#     measure = fields.Field(column_name=_('Physical Find Measurement'), attribute='measurement')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = PhysicalFindingMaster
#         fields = ('fin_type','find_name','measurement','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PhysicalFindingMasterAdmin(ImportExportModelAdmin):
#     resource_class = PhysicalFindingMasterResource
#     list_display =  ('fin_type','find_name','measurement','master_flag',)
#     search_fields = ('find_name','fin_type__find_type','measure__measurement','master_flag',)
#     list_filter = ('find_name',)
# #Physical Finding Master Admin Ends Here 
# 
# 
# 
# 
# 
# #Physical General Admin Starts Here
# class PhysicalGeneralTypeResource(resources.ModelResource):
#     gen_type_name = fields.Field(column_name=_('General Type Name'), attribute='gen_type_name')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = PhysicalGeneralType
#         fields = ('gen_type_name','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PhysicalGeneralTypeAdmin(ImportExportModelAdmin):
#     resource_class = PhysicalGeneralTypeResource
#     list_display =  ('gen_type_name','master_flag',)
#     search_fields = ('gen_type_name','master_flag',)
#     list_filter = ('gen_type_name',)
#     ordering = ('gen_type_name',)
# #Physical General Admin Ends Here    
# 
# #Physical General Master Admin Starts Here
# class PhysicalGeneralMasterResource(resources.ModelResource):
#     gen_type = fields.Field(column_name=_('General Type'), attribute='gen_type', widget=ForeignKeyWidget(PhysicalGeneralType, 'gen_type_name'))
#     gen_name = fields.Field(column_name=_('General Name'), attribute='gen_name')
#     gen_value_type = fields.Field(column_name=_('General Value Type'), attribute='gen_value_type')
#     dropdown_values = fields.Field(column_name=_('Drop Down Values'), attribute='dropdown_values')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = PhysicalGeneralMaster
#         fields = ('gen_type','gen_name','gen_value_type','dropdown_values','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PhysicalGeneralMasterAdmin(ImportExportModelAdmin):
#     resource_class = PhysicalGeneralMasterResource
#     list_display =  ('gen_type','gen_name','gen_value_type','dropdown_values','master_flag',)
#     search_fields = ('gen_name','gen_type__gen_type_name','gen_value_type','master_flag',)
#     list_filter = ('gen_type',)
#     ordering = ('gen_type__gen_type_name',)
# #Physical General Master Admin Ends Here    
# 
# #Investigation Admin Starts Here
# class InvestigationsMasterResource(resources.ModelResource):
#     investg_name = fields.Field(column_name=_('Investigation Name'), attribute='investg_name')
#     investg_desc = fields.Field(column_name=_('Investigation Description'), attribute='investg_desc')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = InvestigationsMaster
#         fields = ('investg_name','investg_desc','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class InvestigationsMasterAdmin(ImportExportModelAdmin):
#     resource_class = InvestigationsMasterResource
#     list_display =  ('investg_name','investg_desc','master_flag',)
#     search_fields = ('investg_name','investg_desc','master_flag',)
#     list_filter = ('investg_name',)
# #Investigation Admin Ends Here
# 
# # Past History Admin Starts Here
# class PastHistoryTypeResource(resources.ModelResource):
#     his_type_name = fields.Field(column_name=_('History Type Name'), attribute='his_type_name')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
# 
#     class Meta:
#         model = PastHistoryType
#         fields = ('his_type_name','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PastHistoryTypeAdmin(ImportExportModelAdmin):
#     resource_class = PastHistoryTypeResource
#     list_display =  ('his_type_name','master_flag',)
#     search_fields = ('his_type_name','master_flag',)
#     list_filter = ('his_type_name',)
# # Past History Admin Ends Here 
# 
# # Past History Master Admin Starts Here
# class PastHistoryMasterResource(resources.ModelResource):
#     his_type = fields.Field(column_name=_('Hospital Type'), attribute='his_type', widget=ForeignKeyWidget(PastHistoryType, 'his_type_name'))
#     his_name = fields.Field(column_name=_('History Name'), attribute='his_name')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = PastHistoryMaster
#         fields = ('his_type','his_name','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class PastHistoryMasterAdmin(ImportExportModelAdmin):
#     resource_class = PastHistoryMasterResource
#     list_display =  ('his_type','his_name','master_flag',)
#     search_fields = ('his_name','his_type__his_type_name','master_flag',)
#     list_filter = ('his_name',)
# # Past History Master Admin Ends Here
# 
# 
# #Miasamatic Analysis Admin Starts Here
# class MiasamaticAnalysisMasterResource(resources.ModelResource):
#     mia_analys_name = fields.Field(column_name=_('Miasamatic Name'), attribute='mia_analys_name')
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#      
#     class Meta:
#         model = MiasamaticAnalysisMaster
#         fields = ('mia_analys_name','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#      
# class MiasamaticAnalysisMasterAdmin(ImportExportModelAdmin):
#     resource_class = MiasamaticAnalysisMasterResource
#     list_display =  ('mia_analys_name','master_flag',)
#     search_fields = ('mia_analys_name','master_flag',)
#     list_filter = ('mia_analys_name',)
# #Miasamatic Analysis Admin Ends Here
# 
# 
# # Investigation Category Master Admin Starts Here
# class InvestigationCategoryMasterResource(resources.ModelResource):
#     investg_cat_name = fields.Field(column_name=_('Investigation Category Name'), attribute='investg_cat_name')
#     investg_cat_unit = fields.Field(column_name=_('Investigation Category Unit'), attribute='investg_cat_unit')
#     investg_mas = fields.Field(column_name=_('Investigation Master'), attribute='investg_mas', widget=ForeignKeyWidget(InvestigationsMaster, 'investg_name'))
#     master_flag = fields.Field(column_name=_('Master Flag'), attribute='master_flag')
#     
#     class Meta:
#         model = InvestigationCategoryMaster
#         fields = ('investg_cat_name','investg_cat_unit','investg_mas','master_flag',)
#         import_id_fields = fields
#         export_order = fields
#     
# class InvestigationCategoryMasterAdmin(ImportExportModelAdmin):
#     resource_class = InvestigationCategoryMasterResource
#     list_display =  ('investg_cat_name','investg_cat_unit','investg_mas','master_flag',)
#     search_fields = ('investg_cat_name',)
# # Investigation Category Master  Admin Ends Here 



admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(EmailTemplate, EmailTemplateAdmin)
admin.site.register(SmsTemplate, SmsTemplateAdmin)
admin.site.register(ClinicalSetting, ClinicalsettingAdmin)
admin.site.register(HospitalMaster, HospitalMasterAdmin)
admin.site.register(CaseCategory, CaseCategoryAdmin)
admin.site.register(CaseCheckListMaster, CaseCheckListMasterAdmin)
admin.site.register(SymptomsMaster, SymptomsMasterAdmin)
admin.site.register(DiseaseMaster, DiseaseMasterAdmin)
admin.site.register(DietsMaster, DietsMasterAdmin)
admin.site.register(HabitsMaster, HabitsMasterAdmin)
admin.site.register(MentalGeneralMaster, MentalGeneralMasterAdmin)
admin.site.register(MedicineMaster, MedicineMasterAdmin)

# admin.site.register(MedicineType, MedicineTypeAdmin)
# admin.site.register(InvestigationsMaster, InvestigationsMasterAdmin)
# admin.site.register(AddonTherapyMaster, AddonTherapyMasterAdmin)
# admin.site.register(FamilyRelationMaster, FamilyRelationMasterAdmin)
# admin.site.register(PhysicalGeneralType, PhysicalGeneralTypeAdmin)
# admin.site.register(PhysicalGeneralMaster, PhysicalGeneralMasterAdmin)
# admin.site.register(PastHistoryType, PastHistoryTypeAdmin)
# admin.site.register(PastHistoryMaster, PastHistoryMasterAdmin)
# admin.site.register(PhysicalFindingType, PhysicalFindingTypeAdmin)
# admin.site.register(PhysicalFindingMaster, PhysicalFindingMasterAdmin)
# admin.site.register(MiasamaticAnalysisMaster, MiasamaticAnalysisMasterAdmin)
# admin.site.register(InvestigationCategoryMaster, InvestigationCategoryMasterAdmin)

