//   mobile menu
$(document).ready(function() {
    var effect = "slide";
    var option = {direction: "left"};
    var duration = 500;
    $(".menu_bar").click(function() {
        $(".navbar_link").show(effect, option, duration);
    });
    $("nav .close").click(function() {
        $(".navbar_link").hide(effect, option, duration);
    });
});

// font increase and decrease

// tooltip

$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});
$(".details a").on('keypress',function(e) {
    var keyCode = e.keyCode || e.which; 
    if (keyCode == 9) {       //if the key pressed was 'tab'...
       e.preventDefault(); 
       //how to focus on the next tab, 
       //remember to select the very first tab when you reach the last tab!
     } 
   });


//    advance and close filter

$(".more_filter").click(function() {
    $("#dashboard").toggleClass("active");
    if(this.innerHTML === "More Filter") {
        this.innerHTML = "Close Filter";
    } else {
        this.innerHTML = "More Filter";
    }
});

/**** search box on 18/6/2020 ******/
/************* search icon jquery ************/
$(document).ready(function() {
    $(".search_icon").click(function() {
        $("#searchBox input").toggleClass("show");
        $("#searchBox input:focus").addClass("show");
        $(this).parent().toggleClass("active");
    });
});
/************* search icon jquery ends ************/
/**** search box ends on 18/6/2020 ******/

/******* add clinical setting ********/
$(document).ready(function() {
    $(".clinical_settings_blk .label_name").click(function() {
       $(this).parent().parent().toggleClass("active"); 
    });
});
/******* add clinical setting ********/

$(".navigation li a").click(function() {
    $(this).parent().toggleClass("show");
});

/****** add clinical sidemenu  *******/
$(document).ready(function() {
    $("#leftArrow").click(function() {
         $(this).parent().parent().toggleClass("collapsed");
    });
    $("#caseSummaryArrow").click(function() {
        $(this).parent().next().toggleClass("active");
        $(this).toggleClass("active");
        $(".add_clinical_case_blk").toggleClass("active");
    });
});
/****** add clinical sidemenu ends  *******/

/***** add symptoms jQuery ********/

$(document).ready(function() {
    $(".symptoms_title .add").click(function() {
        $(this).parent().parent().parent().parent().addClass("active");
    });
    $(".add_btn").click(function() {
        $(this).parent().parent().parent().parent().parent().parent().removeClass("diet_active");
        $(this).parent().parent().parent().parent().parent().parent().addClass("active");
        $('#habit_icon').removeClass("success");
        $('#diet_icon').removeClass("pending");
        $('#habit_icon').addClass("pending");
    });
    $(".add_diet_blk .add_btn").click(function() {
        $(this).parent().parent().parent().parent().parent().parent().addClass("diet_active");
        $('#diet_icon').removeClass("success");
        $('#habit_icon').removeClass("pending");
        $('#diet_icon').addClass("pending");
    });
    $("#edit_habit").click(function() {
        $(this).parent().parent().parent().parent().parent().parent().addClass("Edit_habit_active");
    });
});

/***** add symptoms jQuery ********/
/***** show hide jQuery ********/

$(document).ready(function() {
    $(".show_hide").click(function() {
        $(this).parent().toggleClass("active");
        $(this).parent().parent().parent().toggleClass("active");
    });
    $(".personal_habit_label .show_hide_arrow").click(function() {
        $(this).parent().toggleClass("active");
        $(this).parent().parent().parent().parent().toggleClass("active");
    });
});
/***** show hide jQuery ********/

/******* dropdown **********/
//$(".select_container").chosen({
//    allow_single_deselect: "true"
//});

/********* physical General   ***********/
$(document).ready(function() {
    $("span#physicalGeneralArrow img").click(function() {
        $(this).parent().parent().parent().addClass("active");
        $(this).parent().parent().parent().parent().parent().addClass("active");
        $(".add_clinical_case_blk").addClass("active");
        $(".phy_gen_block_col").removeClass("collapsed");
    });
    $(".physical_general_detail .physical_general_label .label_div .label_image").click(function() {
    $(".physical_general_detail").removeClass("active");
    $(".physical_general_div").removeClass("active");
        $(this).parent().parent().parent().addClass("active");
        $(this).parent().parent().parent().parent().parent().addClass("active");
        $(".add_clinical_case_blk").addClass("active");
        $(".phy_gen_block_col").removeClass("collapsed");
    });
    
    $(".view_close_btn").click(function() {
        $(this).parent().parent().parent().parent().toggleClass("collapsed");
    });
    $('#addAppearence .appetite_block .appetite_radio input[type="radio"], #addAppearence .appetite_block .appetite_radio input[type="checkbox"], #appetite .appetite_block .appetite_radio input[type="radio"], #appetite .appetite_block .appetite_radio input[type="checkbox"],  #thermalReactionBlock input[type="checkbox"]').click(function() {
        
        $(".appetite_radio").removeClass("active");
        if($(this).is(":checked")){
            $("#appetite ").addClass("active");
            $("#addAppearence ").addClass("active");
            $(this).parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#appetite").removeClass("active");
            $("#addAppearence").removeClass("active");
        }
    });
    $('#checkboxPastHistory input[type="checkbox"]').click(function() {
        if($(this).is(":checked")){
            $(this).next().next().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $(this).next().next().removeClass("active");
        }
    });
    $('#appetiteSub input[type="checkbox"]').click(function() {
        if($(this).is(":checked")){
            $(this).parent().next().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $(this).parent().next().removeClass("active");
        }
    });
    $(' .label_checkbox  input[type="checkbox"]').click(function() {
        if($(this).is(":checked")){
            $(this).parent().parent().parent().next().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $(this).parent().parent().parent().next().removeClass("active");
        }
    });
     $(document).ready(function(){
        // If more than 2 Education items, hide the remaining
          $('#addAppearence .appetite_block, #thermalReactionBlock #checkboxLabel').each(function() {
                $(this).find("label.appetite_radio:lt(4)").addClass('shown');
          });
          $('#addAppearence .appetite_block label.appetite_radio, #thermalReactionBlock #checkboxLabel label.appetite_radio').not('.shown').hide();
          $('.show_more').on('click',function(){
              $("#addAppearence .appetite_block label.appetite_radio,  #thermalReactionBlock #checkboxLabel label.appetite_radio ").not('.shown').toggle(300);
              $(this).toggleClass('showLess');
          });
        });
    $('#backArrow  img').click(function() {
        $(".physical_general_detail").removeClass("active");
        $(".physical_general_div").removeClass("active");
        $(".physical_general_appearence").removeClass("active");
    $(".appetite_sub_div").prev().removeClass("active");
          $(".physical_general_detail").removeClass("edit_block_active");
        $(".physical_general_div").removeClass("edit_block");
        $(".appetite_radio").removeClass("active");

    });
 $('.appetite_sub_div .heading img').click(function() {
        $(".physical_general_appearence").removeClass("active");
        $(".appetite_sub_div").prev().removeClass("active");
    });
    $('#thin').click(function() {
        $(".thin").addClass("selected");
        $(this).addClass("selected");
    });
    $('#Emaciated').click(function() {
        $(".Emaciated").addClass("selected");
        $(this).addClass("selected");
    });
    $('#checkboxLabel input[type="checkbox"], #thermalReactionBlock input[type="checkbox"]').click(function() {
        $(".appetite_radio").removeClass("active");
        if($(this).is(":checked")){
            $("#addAppearence, #thermalReactionBlock ").addClass("active");
            $(this).parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#addAppearence, #thermalReactionBlock").removeClass("active");
            $(this).parent().removeClass("active");
        }
    });
       $('.Intolerance_block #checkboxLabel input[type="checkbox"]').click(function() {
        $(".appetite_radio").removeClass("active");
        if($(this).is(":checked")){
            $(".appetite_radio").removeClass("active");
            $("#addAppearence ").removeClass("active");
            $(this).parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#addAppearence").removeClass("active");
            $(this).parent().removeClass("active");
        }
    });
    $(' .stool_radio input[type="radio"]').click(function() {
        if($(this).is(":checked")){
            $(".appetite_radio").removeClass("active");
            $("#addAppearence ").removeClass("active");
            $(this).parent().parent().parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#addAppearence").removeClass("active");
            $(this).parent().parent().parent().addClass("active");
        }
    });
    $('#thermalReactionBlock #thermalReactionBlock .modalities_radio input[type="checkbox"]').click(function() {
        $(".appetite_radio").removeClass("active");
        $(".modalities_radio").removeClass("active");
        if($(this).is(":checked")){
            $(".appetite_radio").removeClass("active");
            $("#thermalReactionBlock ").removeClass("active");
            $(this).parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#thermalReactionBlock").removeClass("active");
            $(this).parent().removeClass("active");
        }
    });
    $('#thermalReactionBlock #thermalReactionBlock .modalities_radio + #checkboxLabel input[type="radio"]').click(function() {
        $(".appetite_radio").removeClass("active");
        if($(this).is(":checked")){
            $(".appetite_radio").removeClass("active");
            $("#thermalReactionBlock ").addClass("active");
            $(this).parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#thermalReactionBlock").removeClass("active");
            $(this).parent().removeClass("active");
        }
    });
    $(' .stool_radio input[type="radio"]').click(function() {
        if($(this).is(":checked")){
            $(".appetite_radio").removeClass("active");
            $("#addAppearence ").removeClass("active");
            $(this).parent().parent().parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $("#addAppearence").removeClass("active");
            $(this).parent().parent().parent().addClass("active");
        }
    });
    /***** miasamatic analysis js *******/
    
    $('.miasmatic_radio input[type="checkbox"]').click(function() {
        if($(this).is(":checked")){
            $(this).parent().parent().addClass("active");
        }
        else if($(this).is(":not(:checked)")){
            $(this).parent().parent().removeClass("active");
        }
    });
    /****** edit block js *******/
    $(".family_history_success .edit img").click(function() {
        $(".phy_gen_block_col").removeClass("collapsed");
        $(this).parent().parent().parent().parent().parent().parent().addClass("edit_block");
        $(this).parent().parent().parent().parent().prev().addClass("edit_block_active");
    });
    /****** edit block js *******/
});
/********* physical General ends  ***********/

/******** obstertric js ***********/
$('#preganencyBlk #checkboxLabel .appetite_radio  input[type="radio"], #preganencyBlk #checkboxLabel .appetite_radio  input[type="checkbox"]').click(function() {
    $(".appetite_radio").removeClass("active");
    if($(this).is(":checked")){
        $(this).parent().addClass("active");
        $("#preganencyBlk").addClass("active");
    }
    else if($(this).is(":not(:checked)")){
        $(this).parent().removeClass("active");
        $("#preganencyBlk").removeClass("active");
    }
});
         $("#addAppearence .para").hide();
          $(" .abortion").hide();
           $(".stillbirth").hide();
            $(".living").hide();
         $(".gravida").hide();
$('#Gravida input[type="checkbox"]').click(function() {
    if($(this).is(":checked")){
       $(".gravida").show();
    }
    else if($(this).is(":not(:checked)")){
        $("#id_gravida_value").empty();
        $(".gravida").hide();
        
    }
});
$(' #Para input[type="checkbox"]').click(function() {
    if($(this).is(":checked")){
       $("#addAppearence .para").show();
    }
    else if($(this).is(":not(:checked)")){
        $("#id_para_value").empty();
        $("#addAppearence .para").hide();
        
    }
});
$(' #abortion input[type="checkbox"]').click(function() {
    if($(this).is(":checked")){
       $(" .abortion").show();
    }
    else if($(this).is(":not(:checked)")){
        $("#id_abortion_value").empty();
        $(" .abortion").hide();
        
    }
});
$(' #stillBirth input[type="checkbox"]').click(function() {
    if($(this).is(":checked")){
       $(".stillbirth").show();
    }
    else if($(this).is(":not(:checked)")){
        $("#id_stillbirth_value").empty();
        $(".stillbirth").hide();
        
    }
});
$(' #living input[type="checkbox"]').click(function() {
    if($(this).is(":checked")){
       $(".living").show();
    }
    else if($(this).is(":not(:checked)")){
        $("#id_living_value").empty();
        $(".living").hide();
    }
});

/******** obstertric js ***********/