var get_courses = new Array();
var table_keshidam = false;
var tedad_goroha = 0;
function reply_click(clicked_id) {

    var button = document.getElementById(clicked_id);
    button.classList.toggle("active");
    var panel = button.nextElementSibling;
    if (panel.style.display === "block") {
        panel.style.display = "none";
    } else {
        add_course(clicked_id);
        panel.style.display = "block";
    }
}

function submit_button(tedad) {
    
    var courses = new Array();
    var index = 0;
    $("input:checkbox[name=chk]:checked").each(function () {
        courses[index] = $(this).attr("id");
        index++;
    });
    $.ajax({
        url: '/add_passed_course',
        type: 'post',
        data: JSON.stringify({passed_courses: courses,username:"temp"}),
        success: function (data) {
            show_remained_table(tedad);
        }
    });
    
}
function show_remained_table(tedad){
    var ted = parseInt(tedad);
    for(i = 0; i < tedad; i++){
        var tb = document.getElementById("remained-unit-" + (i + 1));
        while(tb.rows.length > 1) {
            tb.deleteRow(1);
        }
    }
    

    for(i = 0; i < tedad; i++){
        show_remained(i);
    }
}
function group_number() {
    $.ajax({
        url: '/graduation',
        type: 'post',
        data: JSON.stringify({group: "0", username: "temp"}),
        success: function (data) {
            group_numbers = data.group_count;
            
            create_button(group_numbers);
        },
    });
    
}
function show_remained(index){
    var ind = parseInt(index);
    $.ajax({
        url: '/remained_courses',
        type:'post',
        data: JSON.stringify({table_num: ind + 1, username: "temp"}),
        success: function(data){
        courses = data.remain;
        optional_remained = data.optional_remained;
        create_table(courses, ind, optional_remained, data.all_passed);
        
        },
    });
}
function create_table(courses, index, opt, psd){
    
    if(!table_keshidam){
        for(i = 0; i < tedad_goroha; i++){
            $("#tablee").append(sprintf('<table class="w3-table-all w3-card-4" id="remained-unit-%s">  <caption> ?????? ?????? ???????? %s</caption><tr><th>?????? ??????</th><th>?????????? ????????</th><th>????????????</th></tr></table>', i + 1, i + 1));
        }
         
        table_keshidam = true;
    }
    document.getElementById("vahed_pass_shode").innerHTML = ("?????????? ?????????????? ?????? ?????? : " + psd);
    
    var ind = parseInt(index);
    
    for (i = 0; i < courses.length; i++){
        
        var necessity = "????????";
        if(courses[i].necessity)
            necessity = "??????";
        $("#remained-unit-" + (ind+1)).append(sprintf('<tr><th>%s</th><th>%s</th><th>%s</th></tr>', courses[i].course_name , courses[i].course_unit, necessity));
    }

    $("#remained-unit-" + (ind+1)).append(sprintf('<tr><th>?????? ??????????????</th><th>%s</th><th>??????</th></tr>', opt));

}
function create_button(group_numbers) {
    
    var tedad = parseInt(group_numbers);
    tedad_goroha = tedad;
    for (i = 0; i < tedad; i++) {

        $("#main-content-accordian").append(sprintf('<button class="accordion" id="%s" onClick="reply_click(this.id)">??????????????? ???????? %s</button> <div class="panel"> <ul id="%s"> </ul> </div>', i + 1, i + 1, "course-group-" + (i + 1)));
    }
    $("#main-content-accordian").append(sprintf('<button class="submit-btn" onClick="submit_button(%s)">Submit</button>', tedad));
    //
    for(i = 0; i < tedad; i++){
        show_remained(i);
    }
}

function add_course(groupId) {
    for (var u in get_courses) {
        if (u == groupId)
            return;
    }
    get_courses[groupId] = groupId;
    $.ajax({
        url: '/graduation',
        type: 'post',
        data: JSON.stringify({group: groupId, username: "temp"}),
        success: function (data) {
            var courses = data.user_courses;
            alert(data.info);
            for (i = 0; i < courses.length; i++) {
                var check = "";
                var starred = "";
                if (courses[i].is_passed) {
                    check = "checked";
                }
                if (courses[i].is_starred) {
                    starred = "*";
                }
                $("#course-group-" + groupId).append(sprintf('<li><input type="checkbox" name="chk" id="%s" %s>%s%s</input></li>', courses[i].id, check, starred, courses[i].name));
                $("#course-group-" + groupId + " li:last").data('course', courses[i]);
            }
            $("#course-group-" + groupId).append(sprintf('<li><p>%s</p></li>', data.info));
        },
    });


}
