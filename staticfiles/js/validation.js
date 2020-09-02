$( document ).ready(function() {
    /******* Common Email Format Validation - Starts here *********/
    jQuery.validator.addMethod("email", function(value, element) {
      // allow any non-whitespace characters as the host part
      return this.optional( element ) || /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/.test( value );
    }, 'Please enter a valid email address.');
    
    /******* Common Email Format Validation - Ends here *********/
    
    /******* Common Alphabate Validation - Starts here *********/
    jQuery.validator.addMethod("alpha", function(value, element) {
        return this.optional(element) || /^[a-z\s]+$/i.test(value);
    }, "Please enter Letters only");
    /******* Common Alphabate Validation - Starts here *********/
    
    /******* Common Special Charater Remove Validation - Starts here *********/
    jQuery.validator.addMethod("alphanumeric", function(value, element) {
        return this.optional(element) || /^[0-9a-zA-Z]+$/.test(value);
    }, "Please enter Alphanumeric only");
    /******* Common Special Charater Remove Validation - Starts here *********/
    
    /******* Common Password Validation - Starts here *********/
   $.validator.addMethod("new_password1", function(value) {
      return /^[a-zA-Z0-9!@#$%^&*()_=\[\]{};':"\\|,.<>\/?+-]+$/.test(value)
       && /[a-z]/.test(value) // has a lowercase letter
       && /[A-Z]/.test(value) // has a capitalcase letter
       && /\d/.test(value)//has a digit
       && /[!@#$%^&*()_=\[\]{};':"\\|,.<>\/?+-]/.test(value)// has a special character
      },"Password must consist of Lowercase Letters ,Uppercase Letters, Numbers and special characters");
     /******* Common Password Validation - Ends here *********/
     
    /******* Number with decimal Validation - Starts here *********/
    jQuery.validator.addMethod("decimal_num", function(value, element) {
        return this.optional(element) || /^\d{0,4}(\.\d{0,2})?$/i.test(value);
    }, "You must include two decimal places");
    /******* Number with decimal Validation - Starts here *********/ 
     
     
 //for pdf|DOC|DOCX file upload
    jQuery.validator.addMethod("accept", function(value, element, param) {
     return value.match(new RegExp("." + param + "$"));
    });
   
$.validator.addMethod('filesize', function (value, element, param) {
    return this.optional(element) || (element.files[0].size <= param);
}, 'File size must be less than {0}');
// validation for Login Page starts here
    validator = $("#logn_form").validate({
        rules: {
            username: {
                required: true,
            },
             password: {
                 required: true,
                 //minlength: 6
             },
        },
        messages: {
            username: {
                required: "Username is required"
            },
            password: {
                 required: "Password is required",
                 //minlength: "Password should be atleast 6 characters",
            },
        },
    });
// validation for Login Page ends here


// validation for change Password starts here
    validator = $("#chang_pswd").validate({
        rules: {
            old_password: {
                required: true,
            },
            new_password1: {
                 required: true,
                 minlength: 6,
                 new_password1: true,
             },
            new_password2: {
                required: true,
                equalTo : '#newpassword1'
            },
        },
        messages: {
            old_password: {
                required: "Old Password is required"
            },
            new_password1: {
                 required: "New Password is required",
                 minlength: "Password should be atleast 6 characters",
             },
            new_password2: {
                required: "Confirm Password is required",
                equalTo : "Confirm Password should be same as New Password."
            },
        },
    });
// validation for change Password ends here

// validation for Reset password starts here
    validator = $("#reset_psw").validate({
        rules: {
            new_password1: {
                 required: true,
                 minlength: 6
             },
            new_password2: {
                required: true,
                equalTo : '#newpassword1'
            },
        },
        messages: {
             new_password1: {
                 required: "New Password is required",
                 minlength: "Password should be atleast 6 characters",
             },
            new_password2: {
                required: "Confirm Password is required",
                equalTo : "Confirm Password should be same as New Password."
            },
        },
    });
// validation for Reset password  ends here

// validation for forgot Password starts here
    validator = $("#frgt_pswd").validate({
        rules: {
            email: {
                required: true,
            },
        },
        messages: {
            email: {
                required: "Email is required",
            },
        },
    });
// validation for forgot Password ends here

// validation for Profile iNfo starts here
    validator = $("#profile_info").validate({
        rules: {
            first_name: {
                required: true,
                alpha: true
            },
            mobile_no: {
                digits: true,
                minlength: 10,
                maxlength: 10,
                required: true,
                
            },
            email: {
                required: true,
                email: true,
            },
            last_name: {
                required: true,
                alpha: true
            },
            pincode : {
                required : true,
                maxlength: 6,
                digits: true,
                minlength: 6,
            },
            address_line_1 : {
                required:true,
            },
            address_line_2 : {
                required : true,
            },
            city : {
                required : true,
            },
            state : {
                required : true,
            }
            
        },
        messages: {
            first_name: {
                required: "First Name is required",
            },
            mobile_no: {
                required: "Mobile Number is required",
            },
            last_name : {
                required: "Last Name is required",
            },
            email: {
                required: "Email is required",
            },
            pincode : {
                required: "Pincode is required",
            },
            address_line_1 : {
                required: "Address Line1 is required",
            },
            address_line_2 : {
                required: "Address Line2 is required",
            },
            city : {
                required: "City is required",
            },
            state : {
                required: "State is required",
            },
        },
    });
// validation for forgot Password ends here


// validation for Document Upload starts here

    validator = $("#document_upload").validate({
        rules: {
            group_id : {
                required : true,
            },
            pract_regis_body: {
                required: true,
            },
            pract_state: {
               required: true,
            },
            pract_reg_no: {
                required: true,
                alphanumeric: true
            },
            tnc : {
                required : true,
            }, 
          
        },
        messages: {
            group_id : {
                required : "Role is required",
            },
            pract_regis_body: {
               required: "Registration Body is required",
            },
            pract_state: {
               required: "State is required",
            },
            pract_reg_no: {
                required: "Registration No is required",                
            },
            tnc : {
                required: "Terms & Conditions is required",
            },
        },
   });
   
/***************For terms and condition click on checkbox starts here*************/

    validator = $("#clinical_setting").validate({
        rules: {
            type_of_clinical : {
                required : true,
            },
            clinic_name: {
                required: true,
            },
            address_1: {
                required: true,
            },
            address_2 : {
                required: true,
            },
            city_name  : {
                required: true,
            },
            state_name : {
                required : true,
            },
            pincode : {
                required : true,
            },
        },
        messages: {
            type_of_clinical : {
                required : "Type of Clinical Settings is required",
            },
            clinic_name: {
               required: "Clinic / Hospital Name is required",
            },
            address_1: {
                required: "Clinical/Hospital Address 1 is required",                
            },
            address_2 : {
                required: "Clinical/Hospital Address 2 is required",
            },
            city_name : {
                required: "City is required",
            },
            state_name : {
                required: "State is required",
            },
            pincode : {
                required: "Pincode is required",
            },
        },
   });

// validation for personal history starts here
    validator = $("#add_other_form").validate({
        rules: {
            case_patient_economy_status : {
                required : true,
            },
        },
        messages: {
            case_patient_economy_status : {
                required : "Economy Status is required",
            },
        },
    });
    validator = $("#add_habit_form").validate({
        rules: {
            habit : {
                required : true,
            },
            hab_value : {
                required : true,
            },
            hab_duration: {
                digits: true,
            }
        },
        messages: {
            habit : {
                required : "Habit is required",
            },
            hab_value : {
                required : "Habit Value is required",
            },
        },
    });
    validator = $("#add_diet_form").validate({
        rules: {
            diet : {
                required : true,
            },
            diet_value : {
                required : true,
            },
            diet_duration: {
                digits: true,
            }
        },
        messages: {
            diet : {
                required : "Diet is required",
            },
            diet_value : {
                required : "Diet Value is required",
            },
        },
    });
// validation for personal history ends here


/********* Showing & Hiding Password on click - starts *******/
// function myFunction() {
$(document.body).on('click','.show_password',function(){
  var info_id = $(this).data('info'); 
  var pswd_id = document.getElementById(info_id);
  if (pswd_id.type === "password") {
    pswd_id.type = "text";
  } else {
    pswd_id.type = "password";
  }
});
/********* Showing & Hiding Password on click - ends *******/


// validation for Admin Approval Status starts here
    validator = $("#admin_approval_reg").validate({
        rules: {
            regsr_no: {
                required: true,
            },
            prfile_status_id: {
                required: true,
            },
            message: {
                required: true,
            },
           
        },
        messages: {
            regsr_no: {
                required: "Registration No is required",
            },
            prfile_status_id: {
                required: "Profile status is required",
            },
            message: {
                required: "Message is required",
            },
           }
    });
// validation for Admin Approval Status ends here

// VALIDATION FOR ALL CASE HISTORY TABS --START HERE

// validation for add case details starts here
    validator = $("#add_case_form").validate({
         rules: {
            case_title: {
                required: true,
            },
            case_summary: {
                required: true,
                maxlength:300,
            },
            name_of_institute_unit: {
                required: true,
            },
            case_pract_id: {
                required: true,
            },
            primary_diagnosis: {
                required: true,
            },
         },
         messages: {
            case_title: {
                required: "Title of the Case is required",
            },
            case_summary: {
                required: "Case Summary is required",
                maxlength: "Please don't exceed 300 characters",
            },
            name_of_institute_unit: {
                required: "Name of Institute /Unit /Affiliation is required",
            },
            case_pract_id: {
                required: "Homeopathic Practitioner ID is required",
            },
            primary_diagnosis: {
                required: "Primary Diagnosis is required",
                message:"Plase select the value from dropdown only"
            },
        }
    });
// validation for add case details ends here

// validation for patient details starts here
    validator = $("#patient_details_form").validate({
        rules: {
            case_patient_name: {
                required: true,
                alpha: true
            },
            case_patient_father: {
                alpha: true
            },
            case_patient_age: {
                digits:true,
                required: true,
            },
            case_patient_sex: {
                required: true,
            },
            case_patient_marital_status: {
                required: true,
            },
            case_patient_state :{
                required:true,
            },
            case_patient_mobile :{
                digits:true,
                minlength: 10,
                maxlength: 10,
            },
            case_patient_pin_code :{
                digits:true,
                minlength:6,
                maxlength:6,
            },
        },
        messages: {
            case_patient_name: {
                required: "Name is required",
            },
            case_patient_age: {
                required: "Age is required",
            },
            case_patient_sex: {
                required: "Gender is required",
            },
            case_patient_marital_status: {
                required: "Marital Status is required",
            },
            case_patient_state :{
                required:"State is required",
            },
        }
    });
// validation for patient details ends here

// validation for gynaecological history starts here
   validator = $("#id_menarche_form_id").validate({
        rules: {
            age: {
                digits:true,
            },
        },
        messages: {
            age: {
            },
        }
    });
    validator = $("#id_menop_form_id").validate({
        rules: {
            age: {
                digits:true,
            },
        },
        messages: {
            age: {
            },
        }
    }); 
    validator = $("#id_hyst_form_id").validate({
        rules: {
            age: {
                digits:true,
            },
        },
        messages: {
            age: {
            },
        }
    });
    validator = $("#id_oth_form_id").validate({
        rules: {
            age: {
                digits:true,
            },
        },
        messages: {
            age: {
            },
        }
    });
// validation for gynaecological history ends here

// validation for Obstreric History starts here
    validator = $("#id_obstreric_history_form").validate({
        rules: {
            pbh_his_gravida: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_para: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_abortion: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_stillbirth: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_living: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_period_of_pregnancy: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_lactation_history: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_comp_dur_pregnancy: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_nature_of_labor: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_nature_of_delivery: {
                minlength:2,
                maxlength:150,
            },
            pbh_his_nature_of_puerperium: {
                minlength:2,
                maxlength:150,
            },
        },
        messages: {
            pbh_his_gravida: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_para: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_abortion: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_stillbirth: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_living: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_period_of_pregnancy: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_lactation_history: {
                required: "This field is required",
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_comp_dur_pregnancy: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_nature_of_labor: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_nature_of_delivery: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            pbh_his_nature_of_puerperium: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
        }
    });
// validation for Obstreric History ends here

// validation for Repertorisation starts here
    validator = $("#id_repertorisation_form").validate({
        rules: {
            rep_document: {
                required: true,
            },
            rep_analysis: {
                required: true,
            },
        },
        messages: {
            rep_document: {
                required: "This field is required",
            },
            rep_analysis: {
                required: "This field is required",
            },
        }
    });
    
// validation for present_complaint_form start here
alidator = $("#present_complaint_form").validate({
        rules: {
            comp_symptoms: {
                required: true,
            },
            comp_duration: {
                required: true,
                digits: true,
            },
            comp_duration_type: {
                required: true,
            },
        },
        messages: {
            comp_symptoms: {
                required: "Symptoms is required",
            },
            comp_duration: {
                required: "Duration is required",
            },
            comp_duration_type: {
                required: "Select is required",
            },
        }
    });
// validation for present_complaint_form ends here

// validation for medical management starts here
    validator = $("#medical_management_form").validate({
        rules: {
            prescription_order: {
                required: true,
                minlength:2,
                maxlength:150,
            },
            psrescription: {
                required: true,
                minlength:2,
                maxlength:150,
            },
            potency: {
                required: true,
            },
            dosage: {
                required: true,
            },
            prescription_oridl_scale: {
                minlength:2,
                maxlength:150,
            },
            outcome_of_prev_presc: {
                minlength:2,
                maxlength:150,
            },
            marks_for_improvement: {
                minlength:2,
                maxlength:150,
            },
        },
        messages: {
            prescription_order: {
                required: "This field is required",
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            psrescription: {
                required: "This field is required",
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            potency: {
                required: "This field is required",
            },
            dosage: {
                required: "This field is required",
            },
            prescription_oridl_scale: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            outcome_of_prev_presc: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
            marks_for_improvement: {
                minlength: "Please enter minimum 2 characters.",
                maxlength: "You can't enter more than 150 characters.",
            },
        }
    });
// validation for medical management ends here

validator = $("#id_miasamatic_analysis_form").validate({
        rules: {
            mia_analys_mas: {
                required: true,
            },
        },
        messages: {
            mia_analys_mas: {
                required: "This field is required",
            },
        }
    });
// validation for follow-up starts here
    validator = $("#id_follow_up_form").validate({
        rules: {
            prescription_date: {
                required: true,
            },
            prescription_order: {
                required: true,
            },
            psrescription: {
                required: true,
            },
            potency: {
                required: true,
            },
            dosage: {
                required: true,
            },
        },
        messages: {
            prescription_date: {
                required: "This field is required",
            },
            prescription_order: {
                required: "This field is required",
            },
            psrescription: {
                required: "This field is required",
            },
            potency: {
                required: "This field is required",
            },
            dosage: {
                required: "This field is required",
            },
        }
    });
// validation for follow-up ends here

// validation for add more fields using formset starts here
    jQuery.validator.addClassRules("valid_class", {
        minlength:2,
        maxlength:150,
    });
    
    jQuery.validator.addClassRules("valid_class_require", {
        required: true,
    });
// validation for add more fields using formset ends here
    
//Adding field required using class starts here  
    $(document).ready(function(){
        $.validator.addClassRules({
            valid_class_image_require:{
                      iRequired: true
                     }       
        });
       $.validator.addMethod("iRequired", $.validator.methods.required,"Upload Photo is required");
    });
    
      $(document).ready(function(){
        $.validator.addClassRules({
            valid_class_certification_require:{
                      cRequired: true
                     }       
        });
       $.validator.addMethod("cRequired", $.validator.methods.required,"Registration Certificate is required");
    });
//Adding field required using class ends here  
  
      

// validation for number field fields using formset starts here
$('.number_valid').keyup(function() {
    var inputtxt = $(this).val();
    var pattern = /^[0-9]+$/;
    if(inputtxt.match(pattern)){
        $('#error_message-error').remove();
        return true;
    }
    else{
        var currId = $(this).attr('id');
        $('#'+currId+'-error').remove();
        $('#error_message-error').remove();
        $(this).after('<label id="error_message-error" class="error" for="error_message">Please enter a valid number</label>');
        return false;
    }
});

/****** add clinical sidemenu ends  *******/
$(document).ready(function(){
        $.validator.addClassRules({
            valid_class_keywords_require:{
                      eRequired: true
                     }       
        });
       $.validator.addMethod("eRequired", $.validator.methods.required,"Keyword is required");
    });

// validation for Mental General starts here
    validator = $("#add_case_mental").validate({
        rules: {
            ment_gen_id: {
                required: true,
            },
        },
        messages: {
            ment_gen_id: {
                required: "Symptom is required",
            },
        }
    });
// validation for Mental General ends here

//Physical General Examination Finding starts here
    validator = $("#blood_pressure_physical").validate({
        rules: {
            blood_pressure: {
                required: true,
                decimal_num: true,
            },
        },
        messages: {
            blood_pressure: {
                required: "Blood Pressure is required",
            },
        }
    });
    validator = $("#pulse_pysical_geenral").validate({
        rules: {
            pulse: {
                required: true,
                decimal_num: true,
            },
        },
        messages: {
            pulse: {
                required: "Pulse is required",
            },
        }
    });
    
    validator = $("#respiratory_rate_physcial").validate({
        rules: {
            respiratory_rate: {
                required: true,
                decimal_num: true,
            },
        },
        messages: {
            respiratory_rate: {
                required: "Respiratory Rate is required",
            },
        }
    });
   validator = $("#cyanosis_remarks_physcia").validate({
        rules: {
            cyanosis_remarks: {
                required: true,
            },
        },
        messages: {
            cyanosis_remarks: {
                required: "Remarks is required",
            },
        }
    });
    validator = $("#jaundice_remarks_phisical").validate({
        rules: {
            jaundice_remarks: {
                required: true,
            },
        },
        messages: {
            jaundice_remarks: {
                required: "Remarks is required",
            },
        }
    });
    validator = $("#anaemia_remarks_physical").validate({
        rules: {
            anaemia_remarks: {
                required: true,
            },
        },
        messages: {
            anaemia_remarks: {
                required: "Remarks is required",
            },
        }
    });
    validator = $("#oedema_remarks_physical").validate({
        rules: {
            oedema_remarks: {
                required: true,
            },
        },
        messages: {
            oedema_remarks: {
                required: "Remarks is required",
            },
        }
    });
    validator = $("#lymphadenopathy_remarks_physcial").validate({
        rules: {
            lymphadenopathy_remarks: {
                required: true,
            },
        },
        messages: {
            lymphadenopathy_remarks: {
                required: "Remarks is required",
            },
        }
    });
        validator = $("#clubbing_remarks_physcial").validate({
        rules: {
            clubbing_remarks: {
                required: true,
            },
        },
        messages: {
            clubbing_remarks: {
                required: "Remarks is required",
            },
        }
    });
       validator = $("#id_past_any_recurrent").validate({
        rules: {
            year_of_onset: {
                digits: true,
    //                 required: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    //          messages: {
    //             year_of_onset: {
    //                 required: "Please select year on set",
    //             },
    //         }
    });
      validator = $("#id_past_bronchial").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    validator = $("#id_past_Tuberculosis").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    
    validator = $("#id_past_Chicken").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    validator = $("#id_past_Eczema").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
       
    });
    validator = $("#id_past_Measles").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
       
    });
    validator = $("#id_past_Jaundice").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
        
    });
    validator = $("#id_past_STDs").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    validator = $("#id_past_Cancer").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    validator = $("#id_past_benign").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
    validator = $("#id_past_Others").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
     validator = $("#id_add_hst_supr").validate({
        rules: {
            year_of_onset: {
                digits: true,
            },
             age_of_onset: {
                digits: true,
            },
        },
    });
   validator = $("#id_birth_his_form").validate({
        rules: {
            birth_weight: {
                decimal_num: true,
            },
        },
    });
//Physical General Examination Finding ends here

//OBSTETRIC HISTORY Validation Starts Here
    validator = $("#id_child_form").validate({
        rules: {
            birth_weight: {
                decimal_num: true,
            },
        },
    });
//OBSTETRIC HISTORY Validation Ends Here

// VALIDATION FOR ALL CASE HISTORY TABS --ENDS HERE
});