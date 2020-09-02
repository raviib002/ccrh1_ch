from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget, DateTimeWidget, IntegerWidget
from import_export.admin import ImportMixin, ExportMixin, ImportExportMixin
from import_export.formats import base_formats
from django.forms import forms, ModelForm, Select
from import_export import resources, fields
from master.models import (State, City, ClinicalSetting ,DiseaseMaster, CaseCategory, 
                           CaseCheckListMaster, SymptomsMaster,
                            HabitsMaster, MentalGeneralMaster,
                           )
from user_profile.models import PractDetails
from case_history.models import (
#                                  CaseStatus,
#                                  CaseReviewStatus,
#                                  CaseListingStatus,
#                                  CaseDiagnosis,
#                                  CasePhysicalGeneral,


                                 CaseHistory,
                                 CaseHistoryPatientDetail,
                                 CaseComplaints,
                                 CasePersonalHistory,
                                 CaseMentalGeneral,
                                 CaseFamilyHistory,
                                CasePastHistory,
                                CasePhysicalExaminationFindings,
                                CaseGynaecologicalHistory,
                                
#                                  GynaecologicalHistory,
#                                  CaseObstrericHistory,
#                                  CaseObstrericChildHistory,
#                                  CasePhysicalFindings,
#                                  CaseRepertorisation,
#                                  CaseMiasamaticAnalysis,
#                                  CaseMedicineManagement,
#                                  MedicinePrescriptionMapping,
#                                  PrescriptionSymptomMapping,
#                                  CaseAddonTherapy,
#                                  CaseInvestigation,
#                                  CaseStatusHistory,
#                                  CaseReviewStatusHistory,
#                                  CaseChecklistMapping,
#                                  InvestigationcategoryMapping,
                                )
from django.contrib.auth.models import User
from django.template.defaultfilters import truncatechars




#CaseHistory admin starts here
class CaseHistoryResource(resources.ModelResource):
    class Meta:
        model = CaseHistory
        fields = ('case_id','case_title','keywords','case_summary','case_pract_id',
                  'name_of_institute_unit','diagnosis','case_status','case_reviewer',
                  'case_supervisor','case_category',)
        import_id_fields = fields
        export_order = fields
     
     
class CaseHistoryAdmin(ImportExportModelAdmin):
    resource_class = CaseHistoryResource
    list_display = ('case_id','case_title',)
    search_fields = ('case_id','case_title',)
    list_filter = ('case_id','case_title',)
 
#CaseHistory admin ends here

#CaseComplaints admin starts here
class CaseComplaintsResource(resources.ModelResource):
    class Meta:
        model = CaseComplaints
        fields = ('case','symptoms',)
        import_id_fields = fields
        export_order = fields
    
class CaseComplaintsAdmin(ImportExportModelAdmin):
    resource_class = CaseComplaintsResource
    list_display = ('case','symptoms',)
    search_fields = ('case__case_title','symptoms',)
    list_filter = ('case__case_title','symptoms',)
#CaseComplaints admin ends here

#CasePersonalHistory admin starts here
class CasePersonalHistoryResource(resources.ModelResource):
    class Meta:
        model = CasePersonalHistory
        fields = ('case','habits','diets','case_patient_economy_status','hobbies','evolutionary_history',)
        import_id_fields = fields
        export_order = fields
    
class CasePersonalHistoryAdmin(ImportExportModelAdmin):
    resource_class = CasePersonalHistoryResource
    list_display = ('case','habits','diets','case_patient_economy_status','hobbies','evolutionary_history',)
    search_fields = ('case__case_title','habits','diets','case_patient_economy_status','hobbies','evolutionary_history',)
    list_filter = ('case__case_title','habits','diets','case_patient_economy_status','hobbies','evolutionary_history',)
#CasePersonalHistory admin ends here

#CaseMentalGeneral admin starts here
class CaseMentalGeneralResource(resources.ModelResource):
    class Meta:
        model = CaseMentalGeneral
        fields = ('case','mental_generals',)
        import_id_fields = fields
        export_order = fields
     
     
class CaseMentalGeneralAdmin(ImportExportModelAdmin):
    resource_class = CaseMentalGeneralResource
    list_display = ('case','mental_generals',)
    search_fields = ('case__case_title','mental_generals',)
    list_filter = ('case__case_title',)
#CaseMentalGeneral admin ends here

#CaseFamilyHistory admin starts here
class CaseFamilyHistoryResource(resources.ModelResource):
    class Meta:
        model = CaseFamilyHistory
        fields = ('case','family_history',)
        import_id_fields = fields
        export_order = fields
     
class CaseFamilyHistoryAdmin(ImportExportModelAdmin):
    resource_class = CaseFamilyHistoryResource
    list_display = ('case','family_history',)
    search_fields = ('case__case_title','family_history',)
    list_filter = ('family_history',)
#CaseFamilyHistory admin ends here

#CasePastHistory admin starts here
class CasePastHistoryResource(resources.ModelResource):
    class Meta:
        model = CasePastHistory
        fields = ('case','past_history','history_of_suppression','injuries','accidents','surgery',
                  'history_of_children')
        import_id_fields = fields
        export_order = fields
      
class CasePastHistoryAdmin(ImportExportModelAdmin):
    resource_class = CasePastHistoryResource
    list_display = ('case','past_history','history_of_suppression','injuries','accidents','surgery',
                  'history_of_children')
    search_fields = ('case__case_title',)
    list_filter= ('injuries','accidents','surgery',)
#CasePastHistory admin ends here
#Case Physical Examination Findings Admin Starts Here
class CasePhysicalExaminationFindingsResource(resources.ModelResource):
    class Meta:
        model = CasePhysicalExaminationFindings
        fields = ('case','general_examination','systemic_examination',)
        import_id_fields = fields
        export_order = fields
       
       
class CasePhysicalExaminationFindingsAdmin(ImportExportModelAdmin):
    resource_class = CasePhysicalExaminationFindingsResource
    list_display = ('case','general_examination','systemic_examination',)
    search_fields = ('case__case_title',)
    list_filter = ('case',)
#Case Physical Examination Findings Admin Ends Here
 
#Case Gynaecological History Admin Starts Here
class CaseGynaecologicalHistoryResource(resources.ModelResource):
    class Meta:
        model = CaseGynaecologicalHistory
        fields = ('case','menarche','menstrual_cycle_particulars','abnormal_discharge','menopause',
                  'ho_gynaecological_surgeries','contraceptive_methods')
        import_id_fields = fields
        export_order = fields
       
       
class CaseGynaecologicalHistoryAdmin(ImportExportModelAdmin):
    resource_class = CaseGynaecologicalHistoryResource
    list_display = ('case',)
    search_fields = ('case__case_title',)
    list_filter = ('case',)
#Case Gynaecological History Admin Ends Here




# #CasePhysicalGeneral admin starts here
# class CasePhysicalGeneralResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     hab = fields.Field(column_name=_('Habit'), attribute='hab', widget=ForeignKeyWidget(PhysicalGeneralMaster, 'gen_name'))
#     phygen_value = fields.Field(column_name=_('Physical General Value'), attribute='phygen_value')
#      
#     class Meta:
#         model = CasePhysicalGeneral
#         fields = ('case','hab','phygen_value',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CasePhysicalGeneralAdmin(ImportExportModelAdmin):
#     resource_class = CasePhysicalGeneralResource
#     list_display = ('case','hab','phygen_value',)
#     search_fields = ('case_title','hab__gen_name','phygen_value',)
#     list_filter = ('phygen_value',)
# #CasePhysicalGeneral admin ends here

# #CaseStatus admin starts here
# class CaseStatusResource(resources.ModelResource):
#     cstatus_name = fields.Field(column_name=_('Case Status Name'), attribute='cstatus_name')
#      
#     class Meta:
#         model = CaseStatus
#         fields = ('cstatus_name',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseStatusAdmin(ImportExportModelAdmin):
#     resource_class = CaseStatusResource
#     list_display = ('cstatus_name',)
#     search_fields = ('cstatus_name',)
#     list_filter = ('cstatus_name',)
# #CaseStatus admin ends here
# 
# #CaseReviewStatus admin starts here
# class CaseReviewStatusResource(resources.ModelResource):
#     review_status_name = fields.Field(column_name=_('Case Review Status Name'), attribute='review_status_name')
#      
#     class Meta:
#         model = CaseReviewStatus
#         fields = ('review_status_name',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseReviewStatusAdmin(ImportExportModelAdmin):
#     resource_class = CaseReviewStatusResource
#     list_display = ('review_status_name',)
#     search_fields = ('review_status_name',)
#     list_filter = ('review_status_name',)
# #CaseReviewStatus admin ends here
# 
# #CaseListingStatus admin starts here
# class CaseListingStatusResource(resources.ModelResource):
#     listing_status_name = fields.Field(column_name=_('Case Listing Status Name'), attribute='listing_status_name')
#      
#     class Meta:
#         model = CaseListingStatus
#         fields = ('listing_status_name',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseListingStatusAdmin(ImportExportModelAdmin):
#     resource_class = CaseListingStatusResource
#     list_display = ('listing_status_name',)
#     search_fields = ('listing_status_name',)
#     list_filter = ('listing_status_name',)
# #CaseListingStatus admin ends here

# #CaseDiagnosis admin starts here 
# class CaseDiagnosisResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case Title'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     dis = fields.Field(column_name=_('Case Disease'), attribute='dis', widget=ForeignKeyWidget(DiseaseMaster, 'dis_name'))
#     is_primary = fields.Field(column_name=_('Is Primary'), attribute='is_primary')
# 
#     class Meta:
#         model = CaseDiagnosis
#         fields = ('case','dis','is_primary')
#         import_id_fields = fields
#         export_order = fields
#     
# class CaseDiagnosisAdmin(ImportExportModelAdmin):
#     resource_class = CaseDiagnosisResource
#     list_display = ('case','dis','is_primary',)
#     search_fields = ('case__case_title', 'dis__dis_name', 'is_primary',)
#     list_filter = ('is_primary',)
# #CaseDiagnosis admin ends here
# #GynaecologicalHistory admin starts here
# class GynaecologicalHistoryResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     menarche_date_age = fields.Field(column_name=_('Menarche Date Age'), attribute='menarche_date_age')
#     menst_lmp = fields.Field(column_name=_('Last Menstrual Period'), attribute='menst_lmp')
#     menst_cycle = fields.Field(column_name=_('Menstrual Cycle'), attribute='menst_cycle')
#     menst_duration = fields.Field(column_name=_('Menstrual Duration'), attribute='menst_duration')
#     menst_quantity = fields.Field(column_name=_('Menstrual Quantity'), attribute='menst_quantity')
#     menst_colour = fields.Field(column_name=_('Menstrual Colour'), attribute='menst_colour')
#     menst_odur = fields.Field(column_name=_('Menstrual Odour'), attribute='menst_odur')
#     menst_character = fields.Field(column_name=_('Menstrual Character'), attribute='menst_character')
#     menst_complaints_b_d_a_menses = fields.Field(column_name=_('Menstrual Complaints B D A Menses'), attribute='menst_complaints_b_d_a_menses')
#     menst_leucorrhea = fields.Field(column_name=_('Menstrual Leucorrhea'), attribute='menst_leucorrhea')
#     menst_surgery = fields.Field(column_name=_('Menstrual Surgery'), attribute='menst_surgery')
#     menopause_date_age = fields.Field(column_name=_('MENOPAUSE Date/Age'), attribute='menopause_date_age')
#     ho_hysterectomy = fields.Field(column_name=_('H/O Hysterectomy'), attribute='ho_hysterectomy')
#      
#     class Meta:
#         model = GynaecologicalHistory
#         fields = ('case','menarche_date_age','menst_lmp','menst_cycle',
#                   'menst_duration','menst_quantity','menst_colour','menst_odur',
#                   'menst_character','menst_complaints_b_d_a_menses','menst_leucorrhea','menst_surgery',
#                   'menopause_date_age', 'ho_hysterectomy', )
#         import_id_fields = fields
#         export_order = fields
#      
# class GynaecologicalHistoryAdmin(ImportExportModelAdmin):
#     resource_class = GynaecologicalHistoryResource
#     list_display = ('case','menst_cycle','menst_quantity','menst_colour','menst_odur','menst_character',)
#     search_fields = ('case_title','menst_cycle','menst_quantity','menst_colour','menst_odur','menst_character',)
#     list_filter = ('menst_quantity','menst_colour','menst_odur','menst_character',)
# #GynaecologicalHistory admin ends here
# 
# #CaseObstrericHistory admin starts here
# class CaseObstrericHistoryResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     pbh_his_gravida = fields.Field(column_name=_('Pbh Gravida Histroy'), attribute='pbh_his_gravida')
#     pbh_his_para = fields.Field(column_name=_('Pbh Para History'), attribute='pbh_his_para')
#     pbh_his_abortion = fields.Field(column_name=_('Pbh Abortion History'), attribute='pbh_his_abortion')
#     pbh_his_stillbirth = fields.Field(column_name=_('Pbh Stillbirth History'), attribute='pbh_his_stillbirth')
#     pbh_his_living = fields.Field(column_name=_('Pbh Living History'), attribute='pbh_his_living')
#     pbh_his_period_of_pregnancy = fields.Field(column_name=_('Pbh Pregnancy Histroy'), attribute='pbh_his_period_of_pregnancy')
#     pbh_his_lactation_history = fields.Field(column_name=_('Pbh Lactation History'), attribute='pbh_his_lactation_history')
#     pbh_his_comp_dur_pregnancy = fields.Field(column_name=_('Pbh Complaints During Pregnancy History'), attribute='pbh_his_comp_dur_pregnancy')
#     pbh_his_nature_of_labor = fields.Field(column_name=_('Pbh Nature of Labour History'), attribute='pbh_his_nature_of_labor')
#     pbh_his_nature_of_delivery = fields.Field(column_name=_('Pbh Nature of Delivery History'), attribute='pbh_his_nature_of_delivery')
#     pbh_his_nature_of_puerperium = fields.Field(column_name=_('Pbh Nature of Puerperium History'), attribute='pbh_his_nature_of_puerperium')
#      
#     class Meta:
#         model = CaseObstrericHistory
#         fields = ('case','pbh_his_gravida','pbh_his_para','pbh_his_abortion',
#                   'pbh_his_stillbirth','pbh_his_living','pbh_his_period_of_pregnancy','pbh_his_lactation_history',
#                   'pbh_his_comp_dur_pregnancy','pbh_his_nature_of_labor','pbh_his_nature_of_delivery','pbh_his_nature_of_puerperium',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseObstrericHistoryAdmin(ImportExportModelAdmin):
#     resource_class = CaseObstrericHistoryResource
#     list_display = ('case','pbh_his_gravida','pbh_his_para','pbh_his_abortion','pbh_his_stillbirth',)
#     search_fields = ('case_title','pbh_his_gravida','pbh_his_para','pbh_his_abortion','pbh_his_stillbirth',)
#     list_filter = ('pbh_his_gravida',)
# #CaseObstrericHistory admin ends here
# 
# #CaseObstrericChildHistory admin starts here
# class CaseObstrericChildHistoryResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     chd_his_child = fields.Field(column_name=_('Child History'), attribute='chd_his_child')
#     chd_his_alive = fields.Field(column_name=_('Is Alive'), attribute='chd_his_alive')
#     chd_his_causeofdeath = fields.Field(column_name=_('Cause of Death'), attribute='chd_his_causeofdeath')
#     chd_his_birthweight = fields.Field(column_name=_('Birth Weight'), attribute='chd_his_birthweight')
#      
#     class Meta:
#         model = CaseObstrericChildHistory
#         fields = ('case','chd_his_child','chd_his_alive','chd_his_causeofdeath','chd_his_birthweight',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseObstrericChildHistoryAdmin(ImportExportModelAdmin):
#     resource_class = CaseObstrericChildHistoryResource
#     list_display = ('case','chd_his_child','chd_his_alive','chd_his_causeofdeath','chd_his_birthweight',)
#     search_fields = ('case__case_title','chd_his_child','chd_his_alive','chd_his_causeofdeath','chd_his_birthweight',)
#     list_filter = ('chd_his_alive',)
# #CaseObstrericChildHistory admin ends here
# 
# 
# #CaseRepertorisation admin starts here
# class CaseRepertorisationResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     rep_document = fields.Field(column_name=_('Repertorisation  Document'), attribute='rep_document')
#     rep_analysis = fields.Field(column_name=_('Repertorisation Analysis'), attribute='rep_analysis')
#      
#     class Meta:
#         model = CaseRepertorisation
#         fields = ('case','rep_document','rep_analysis',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseRepertorisationAdmin(ImportExportModelAdmin):
#     resource_class = CaseRepertorisationResource
#     list_display = ('case','rep_document','rep_analysis',)
#     search_fields = ('case_case_title','rep_document','rep_analysis',)
#     list_filter = ('rep_analysis',)
# #CaseRepertorisation admin ends here
# 
# #CaseMiasamaticAnalysis admin starts here
# class CaseMiasamaticAnalysisResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     mia_analys_mas = fields.Field(column_name=_('Miasamatic Analysis'), attribute='mia_analys_mas', widget=ForeignKeyWidget(MiasamaticAnalysisMaster, 'mia_analys_name'))
#     mia_analys_value = fields.Field(column_name=_('Miasamatic Analysis Value'), attribute='mia_analys_value')
#     mia_details = fields.Field(column_name=_('Miasamatic Details'), attribute='mia_details')
#       
#     class Meta:
#         model = CaseMiasamaticAnalysis
#         fields = ('case','mia_analys_mas','mia_analys_value','mia_details',)
#         import_id_fields = fields
#         export_order = fields
#       
# class CaseMiasamaticAnalysisAdmin(ImportExportModelAdmin):
#     resource_class = CaseMiasamaticAnalysisResource
#     list_display = ('case','mia_analys_mas','mia_analys_value',)
#     search_fields = ('case__case_title','mia_analys_mas__mia_analys_name','mia_analys_value',)
#     list_filter = ('mia_analys_mas','mia_analys_value')
# #CaseMiasamaticAnalysis admin ends here
# 
# 
# #CaseInvestigation admin starts here
# class CaseInvestigationResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     investg_mas = fields.Field(column_name=_('Investigation'), attribute='investg_mas', widget=ForeignKeyWidget(InvestigationsMaster, 'investg_name'))
#     investg_value = fields.Field(column_name=_('Investigation Value'), attribute='investg_value')
#     investg_file = fields.Field(column_name=_('Investigation File'), attribute='investg_file')
#     
#     class Meta:
#         model = CaseInvestigation
#         fields = ('case','investg_mas','investg_value','investg_file',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseInvestigationAdmin(ImportExportModelAdmin):
#     resource_class = CaseInvestigationResource
#     list_display = ('case','investg_mas','investg_value','investg_file',)
#     search_fields = ('case__case_title','investg_mas__investg_name','investg_value','investg_file',)
#     list_filter = ('investg_mas',)
# #CaseInvestigation admin ends here
# 
# 
# #CaseMedicineManagement admin starts here
# class CaseMedicineManagementResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     prescription_date = fields.Field(column_name=_('Prescription Date'), attribute='prescription_date')
#     prescription_order = fields.Field(column_name=_('Prescription Order'), attribute='prescription_order')
#     prescription_oridl_scale = fields.Field(column_name=_('Prescription ORIDL Scale'), attribute='prescription_oridl_scale')
#     outcome_of_prev_presc = fields.Field(column_name=_('Outcome of Previous Prescription'), attribute='outcome_of_prev_presc')
#     marks_for_improvement = fields.Field(column_name=_('Marks for Improvement'), attribute='marks_for_improvement')
#     
#      
#     class Meta:
#         model = CaseMedicineManagement
#         fields = ('case','prescription_date','prescription_order','prescription_oridl_scale','outcome_of_prev_presc','marks_for_improvement',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseMedicineManagementAdmin(ImportExportModelAdmin):
#     resource_class = CaseMedicineManagementResource
#     list_display = ('case','prescription_date','prescription_order','prescription_oridl_scale',)
#     search_fields = ('case__case_title','prescription_date','prescription_order','prescription_oridl_scale',)
# #CaseMedicineManagement admin ends here
# 
# #MedicinePrescriptionMapping admin starts here
# class MedicinePrescriptionMappingResource(resources.ModelResource):
#     medi_mgnt = fields.Field(column_name=_('Medical Management'), attribute='medi_mgnt', widget=ForeignKeyWidget(CaseMedicineManagement, 'id'))
#     prescription = fields.Field(column_name=_('Prescription'), attribute='prescription', widget=ForeignKeyWidget(MedicineMaster, 'med_name'))
#     potency = fields.Field(column_name=_('Potency'), attribute='potency')
#     dosage = fields.Field(column_name=_('Dosage'), attribute='dosage')
#     
#     class Meta:
#         model = MedicinePrescriptionMapping
#         fields = ('medi_mgnt','prescription','potency','dosage',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class MedicinePrescriptionMappingAdmin(ImportExportModelAdmin):
#     resource_class = MedicinePrescriptionMappingResource
#     list_display = ('medi_mgnt','prescription','potency','dosage',)
#     search_fields = ('medi_mgnt__prescription_order','prescription','potency','dosage',)
# #MedicinePrescriptionMapping admin ends here
# 
# #PrescriptionSymptomMapping admin starts here
# class PrescriptionSymptomMappingResource(resources.ModelResource):
#     medi_pres_map = fields.Field(column_name=_('Medical Prescription'), attribute='medi_pres_map', widget=ForeignKeyWidget(MedicinePrescriptionMapping, 'id'))
#     symptom = fields.Field(column_name=_('Symptoms'), attribute='symptom', widget=ForeignKeyWidget(SymptomsMaster, 'sym_name'))
#     
#     class Meta:
#         model = PrescriptionSymptomMapping
#         fields = ('medi_pres_map','symptom',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class PrescriptionSymptomMappingAdmin(ImportExportModelAdmin):
#     resource_class = PrescriptionSymptomMappingResource
#     list_display = ('medi_pres_map','symptom',)
#     search_fields = ('medi_pres_map','symptom',)
# #PrescriptionSymptomMapping admin ends here
# 
# #CaseAddonTherapy admin starts here
# class CaseAddonTherapyResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     addon_order = fields.Field(column_name=_('Addon Therapy Order'), attribute='addon_order')
#     addon_thrpy_mas = fields.Field(column_name=_('Add-on Therapy'), attribute='addon_thrpy_mas', widget=ForeignKeyWidget(AddonTherapyMaster, 'thrpy_name'))
#     duration_tamper_homeo = fields.Field(column_name=_('Duration Temper Homeo'), attribute='duration_tamper_homeo')
#     medicine_name = fields.Field(column_name=_('Medicine Name'), attribute='medicine_name')
#     medicine_dosage = fields.Field(column_name=_('Medicine Dosage'), attribute='medicine_dosage')
#     duration_other_therapy = fields.Field(column_name=_('Duration of other therapy(Year/Months/Days)'), attribute='duration_other_therapy')
#     duration_after_which_other_therapy = fields.Field(column_name=_('Duration after which other therapy (Allopathy/Ayurveda/ Siddha etc) was tapered after homoeopathic treatment'), attribute='duration_after_which_other_therapy')
#     
#     class Meta:
#         model = CaseAddonTherapy
#         fields = ('case','addon_order','addon_thrpy_mas','duration_tamper_homeo','medicine_name','medicine_dosage','duration_other_therapy','duration_after_which_other_therapy')
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseAddonTherapyAdmin(ImportExportModelAdmin):
#     resource_class = CaseAddonTherapyResource
#     list_display = ('case','addon_thrpy_mas','duration_tamper_homeo','medicine_name','medicine_dosage','addon_order',)
#     search_fields = ('case__case_title','addon_thrpy_mas__thrpy_name','duration_tamper_homeo','medicine_name','medicine_dosage',)
#     list_filter = ('addon_thrpy_mas','duration_tamper_homeo',)
# #CaseAddonTherapy admin ends here
# 
# 
# #CaseStatusHistory admin starts here
# class CaseStatusHistoryResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     case_status = fields.Field(column_name=_('Case Status'), attribute='case_status')
#     case_remarks = fields.Field(column_name=_('Case Remarks'), attribute='case_remarks')
#     
#     class Meta:
#         model = CaseStatusHistory
#         fields = ('case','case_status','case_remarks',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseStatusHistoryAdmin(ImportExportModelAdmin):
#     resource_class = CaseStatusHistoryResource
#     list_display = ('case','case_status','case_remarks',)
#     search_fields = ('case','case_status','case_remarks',)
#     list_filter = ('case_remarks',)
# #CaseStatusHistory admin ends here
# 
# #CaseReviewStatusHistory admin starts here
# class CaseReviewStatusHistoryResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     case_review_status = fields.Field(column_name=_('Case Review Status'), attribute='case_review_status', widget=ForeignKeyWidget(CaseReviewStatus, 'review_status_name'))
#     case_review_remarks = fields.Field(column_name=_('Case Review Remarks'), attribute='case_review_remarks')
#     
#     class Meta:
#         model = CaseReviewStatusHistory
#         fields = ('case','case_review_status','case_review_remarks',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseReviewStatusHistoryAdmin(ImportExportModelAdmin):
#     resource_class = CaseReviewStatusHistoryResource
#     list_display = ('case_review_status','case_review_remarks',)
#     search_fields = ('case__case_title','case_review_status__review_status_name','case_review_remarks',)
#     list_filter = ('case_review_status',)
# #CaseReviewStatusHistory admin ends here
# 
# #CaseChecklistMapping admin starts here
# class CaseChecklistMappingResource(resources.ModelResource):
#     case = fields.Field(column_name=_('Case History'), attribute='case', widget=ForeignKeyWidget(CaseHistory, 'case_title'))
#     checklist = fields.Field(column_name=_('Case CheckList'), attribute='checklist')
#     checklist_value = fields.Field(column_name=_('Checklist Value'), attribute='checklist_value')
#     
#     class Meta:
#         model = CaseChecklistMapping
#         fields = ('case','checklist','checklist_value',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class CaseChecklistMappingAdmin(ImportExportModelAdmin):
#     resource_class = CaseChecklistMappingResource
#     list_display = ('case','checklist','checklist_value',)
#     search_fields = ('case','checklist','checklist_value',)
#     list_filter = ('checklist_value',)
# #CaseChecklistMapping admin ends here
# 
# 
# #Investigation Mapping admin starts here
# class InvestigationMappingResource(resources.ModelResource):
#     investg = fields.Field(column_name=_('Investigation'), attribute='investg', widget=ForeignKeyWidget(CaseInvestigation, 'investg_mas__investg_name'))
#     investg_cat = fields.Field(column_name=_('Investigation Category'), attribute='investg_cat', widget=ForeignKeyWidget(InvestigationCategoryMaster, 'investg_cat_name'))
#     investg_cat_value = fields.Field(column_name=_('Investigation Category Value'), attribute='investg_cat_value')
#     
#     class Meta:
#         model = InvestigationcategoryMapping
#         fields = ('investg','investg_cat','investg_cat_value',)
#         import_id_fields = fields
#         export_order = fields
#      
#      
# class InvestigationCategoryMappingAdmin(ImportExportModelAdmin):
#     resource_class = InvestigationMappingResource
#     list_display = ('investg','investg_cat','investg_cat_value',)
#     search_fields =('investg','investg_cat','investg_cat_value',)
# #CaseChecklistMapping admin ends here



admin.site.register(CaseHistory, CaseHistoryAdmin)
admin.site.register(CaseHistoryPatientDetail)
admin.site.register(CaseComplaints, CaseComplaintsAdmin)
admin.site.register(CasePersonalHistory, CasePersonalHistoryAdmin)
admin.site.register(CaseMentalGeneral, CaseMentalGeneralAdmin)
admin.site.register(CaseFamilyHistory, CaseFamilyHistoryAdmin)

admin.site.register(CasePastHistory)
admin.site.register(CasePhysicalExaminationFindings, CasePhysicalExaminationFindingsAdmin)
admin.site.register(CaseGynaecologicalHistory, CaseGynaecologicalHistoryAdmin)

# admin.site.register(CaseStatus, CaseStatusAdmin)
# admin.site.register(CaseReviewStatus, CaseReviewStatusAdmin)
# admin.site.register(CaseListingStatus, CaseListingStatusAdmin)
# admin.site.register(CaseDiagnosis, CaseDiagnosisAdmin)
# admin.site.register(CasePhysicalGeneral, CasePhysicalGeneralAdmin)
# admin.site.register(CaseObstrericHistory, CaseObstrericHistoryAdmin)
# admin.site.register(CaseObstrericChildHistory, CaseObstrericChildHistoryAdmin)
# admin.site.register(CasePhysicalFindings, CasePhysicalFindingsAdmin)
# admin.site.register(CaseRepertorisation, CaseRepertorisationAdmin)
# admin.site.register(CaseMiasamaticAnalysis, CaseMiasamaticAnalysisAdmin)
# admin.site.register(CaseMedicineManagement, CaseMedicineManagementAdmin)
# admin.site.register(MedicinePrescriptionMapping, MedicinePrescriptionMappingAdmin)
# admin.site.register(PrescriptionSymptomMapping, PrescriptionSymptomMappingAdmin)
# admin.site.register(CaseAddonTherapy, CaseAddonTherapyAdmin)
# admin.site.register(CaseInvestigation, CaseInvestigationAdmin)
# admin.site.register(CaseStatusHistory, CaseStatusHistoryAdmin)
# admin.site.register(CaseReviewStatusHistory, CaseReviewStatusHistoryAdmin)
# admin.site.register(CaseChecklistMapping, CaseChecklistMappingAdmin)
# admin.site.register(InvestigationcategoryMapping, InvestigationCategoryMappingAdmin)
