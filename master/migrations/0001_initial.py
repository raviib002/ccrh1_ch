# Generated by Django 2.2.11 on 2020-09-02 13:41

import audit_log.models.fields
import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import djongo.models.fields
import master.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=100, verbose_name='City Name')),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'City',
                'db_table': 'ccrh_city_master',
            },
        ),
        migrations.CreateModel(
            name='ClinicalSetting',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('cs_name', models.CharField(max_length=100, verbose_name='Clinical Setting Name')),
            ],
            options={
                'verbose_name': 'Clinical Setting',
                'verbose_name_plural': 'Clinical Setting',
                'db_table': 'ccrh_pract_clinical_setting_master',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('state_name', models.CharField(max_length=100, verbose_name='State Name')),
                ('country_id', models.CharField(choices=[('1', 'INDIA')], default=1, max_length=1, verbose_name='Country Name')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'State',
                'db_table': 'ccrh_state_master',
            },
        ),
        migrations.CreateModel(
            name='SymptomsMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('sym_name', models.TextField(verbose_name='Symptoms Name')),
                ('sym_desc', models.TextField(blank=True, null=True, verbose_name='Symptoms Description')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SymptomsMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SymptomsMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Symptoms Master ',
                'verbose_name_plural': 'Symptoms Master',
                'db_table': 'ccrh_symptoms_master',
            },
        ),
        migrations.CreateModel(
            name='SmsTemplate',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('sms_code', models.CharField(max_length=10, verbose_name='SMS Code')),
                ('sms_text', models.TextField(help_text='Note : Do not change the text inside curly braces {}', verbose_name='SMS Text')),
                ('trigger_point', models.TextField(blank=True, null=True, verbose_name='Trigger Point')),
                ('sent_to', models.CharField(blank=True, max_length=200, null=True, verbose_name='Send To')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SmsTemplateCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='SmsTemplateUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'SMS Template',
                'db_table': 'ccrh_sms_template',
            },
        ),
        migrations.CreateModel(
            name='MentalGeneralMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('mental_general_val', models.CharField(max_length=250, verbose_name='Mental General Value')),
                ('mental_desc', models.TextField(blank=True, null=True, verbose_name='Mental General Description')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='MentalGeneralMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='MentalGeneralMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Mental General Master',
                'verbose_name_plural': 'Mental General Master',
                'db_table': 'ccrh_mental_general_master',
            },
        ),
        migrations.CreateModel(
            name='MedicineMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('med_name', models.CharField(max_length=100, verbose_name='Medicine Name')),
                ('medicine_type', djongo.models.fields.EmbeddedField(model_container=master.models.MedicineType, null=True)),
                ('potencies', djongo.models.fields.EmbeddedField(model_container=master.models.Potencies, null=True)),
                ('internal_application', models.TextField(blank=True, null=True, verbose_name='Internal Application')),
                ('external_application', models.TextField(blank=True, null=True, verbose_name='External Application')),
                ('sources', djongo.models.fields.EmbeddedField(model_container=master.models.Sources, null=True)),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='MedicineMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='MedicineMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Medicine Master ',
                'verbose_name_plural': 'Medicine Master',
                'db_table': 'ccrh_medicine_master',
            },
        ),
        migrations.CreateModel(
            name='HospitalMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('hospital_name', models.CharField(max_length=250, verbose_name='Hospital Name')),
                ('address_1', models.TextField(blank=True, null=True, verbose_name='Address 1')),
                ('address_2', models.TextField(blank=True, null=True, verbose_name='Address 2')),
                ('pincode', models.BigIntegerField(blank=True, null=True, verbose_name='Pin Code')),
                ('permitted_seats', models.TextField(blank=True, null=True, verbose_name='Permitted Seats')),
                ('master_flag', models.BooleanField(default=False, verbose_name='Master Flag')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.City', verbose_name='City')),
                ('hospital_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.ClinicalSetting', verbose_name='Hospital Type')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.State', verbose_name='State')),
            ],
            options={
                'verbose_name': 'Hospital Master ',
                'verbose_name_plural': 'Hospital Master',
                'db_table': 'ccrh_hospital_master',
            },
        ),
        migrations.CreateModel(
            name='HabitsMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('hab_name', models.CharField(max_length=100, verbose_name='Habit Name')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='HabitsMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='HabitsMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Habit Master ',
                'verbose_name_plural': 'Habit Master',
                'db_table': 'ccrh_habits_master',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('email_code', models.CharField(max_length=10, verbose_name='Email Code')),
                ('email_subject', models.TextField(verbose_name='Email Subject')),
                ('email_body', ckeditor.fields.RichTextField(help_text='Note : Do not change the text inside curly braces {}', verbose_name='Email Body')),
                ('sent_to', models.CharField(blank=True, max_length=200, null=True, verbose_name='Send To')),
                ('trigger_point', models.TextField(blank=True, null=True, verbose_name='Trigger Point')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='EmailTemplateCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='EmailTemplateUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Email Template',
                'db_table': 'ccrh_email_template',
            },
        ),
        migrations.CreateModel(
            name='DiseaseMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tn_ancestors_pks', models.TextField(blank=True, default='', editable=False, verbose_name='Ancestors pks')),
                ('tn_ancestors_count', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Ancestors count')),
                ('tn_children_pks', models.TextField(blank=True, default='', editable=False, verbose_name='Children pks')),
                ('tn_children_count', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Children count')),
                ('tn_depth', models.PositiveSmallIntegerField(default=0, editable=False, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Depth')),
                ('tn_descendants_pks', models.TextField(blank=True, default='', editable=False, verbose_name='Descendants pks')),
                ('tn_descendants_count', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Descendants count')),
                ('tn_index', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Index')),
                ('tn_level', models.PositiveSmallIntegerField(default=1, editable=False, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Level')),
                ('tn_priority', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(9999)], verbose_name='Priority')),
                ('tn_order', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Order')),
                ('tn_siblings_pks', models.TextField(blank=True, default='', editable=False, verbose_name='Siblings pks')),
                ('tn_siblings_count', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='Siblings count')),
                ('dis_name', models.CharField(max_length=250, verbose_name='Category / Sub-Category / Disease Name')),
                ('icd_range', models.CharField(blank=True, max_length=50, null=True, verbose_name='ICD Code Range')),
                ('dis_icd_code', models.CharField(blank=True, max_length=50, null=True, verbose_name='ICD Code')),
                ('dis_desc', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('dis_mapped', models.TextField(blank=True, help_text='Kindly enter comma separated ICD Code without any other special chars like spaces Example - M01.3,G01,M90.2,J17.0,N16.0', null=True, verbose_name='Cross Referencing Disease Code')),
                ('tn_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tn_children', to='master.DiseaseMaster', verbose_name='Parent')),
            ],
            options={
                'verbose_name': 'Disease Master',
                'verbose_name_plural': 'Disease Master',
                'db_table': 'ccrh_disease_master',
                'ordering': ['tn_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DietsMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('diet_name', models.CharField(max_length=100, verbose_name='Diet Name')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='DietsMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='DietsMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Diet Master',
                'verbose_name_plural': 'Diet Master',
                'db_table': 'ccrh_diets_master',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='master.State', verbose_name='State Name'),
        ),
        migrations.CreateModel(
            name='CaseCheckListMaster',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('checklist_name', models.CharField(max_length=150, verbose_name='CheckList Name')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CaseCheckListMasterCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CaseCheckListMasterUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Case CheckList Master',
                'verbose_name_plural': 'Case CheckList Master',
                'db_table': 'case_checklist_master',
            },
        ),
        migrations.CreateModel(
            name='CaseCategory',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=50, verbose_name='Category Name')),
                ('icd_code', models.CharField(help_text='EX: A00-B99', max_length=50, verbose_name='ICD Code')),
                ('master_flag', models.BooleanField(default=True, verbose_name='Master Flag')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('created_by', audit_log.models.fields.CreatingUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CaseCategoryCreatedBy', to=settings.AUTH_USER_MODEL)),
                ('updated_by', audit_log.models.fields.LastUserField(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='CaseCategoryUpdatedBy', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Case Category',
                'verbose_name_plural': 'Case Category',
                'db_table': 'case_category',
            },
        ),
        migrations.AddIndex(
            model_name='diseasemaster',
            index=models.Index(fields=['dis_name', 'dis_icd_code'], name='ccrh_diseas_dis_nam_18efcd_idx'),
        ),
    ]
