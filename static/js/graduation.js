var get_courses = new Array();

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

function submit_button() {
    var courses = new Array();
    var index = 0;
    $("input:checkbox[name=chk]:checked").each(function () {
        courses[index] = $(this).attr("id");
        index++;
    });
    $.ajax({
        url: '/passed_course',
        type: 'post',
        data: JSON.stringify({passed_courses: courses}),
        success: function (data) {

        }
    });

}

function group_number() {
    $.ajax({
        url: '/graduation',
        type: 'post',
        data: JSON.stringify({group: "0", user: "temp"}),
        success: function (data) {
            group_numbers = data.group_count;
            
            create_button(group_numbers);
        },
    });
    show_remained();
}
function show_remained(){
    $.ajax({
        url: '/remained_courses',
        success: function(data){
        courses = data.remain;
        create_table(courses);
        
        },
    });
}
function create_table(courses){
    for (i = 0; i < courses.length; i++){
        var necessity = "نیست";
        if(courses[i].necessity)
            necessity = "هست";
        $("#remained-unit").append(sprintf('<tr><th>%s</th><th>%s</th><th>%s</th></tr>', courses[i].course_name , courses[i].course_unit, necessity));
    }
}
function create_button(group_numbers) {
    
    var tedad = parseInt(group_numbers);
    for (i = 0; i < tedad; i++) {

        $("#main-content-accordian").append(sprintf('<button class="accordion" id="%s" onClick="reply_click(this.id)">درس‌های گروه %s</button> <div class="panel"> <ul id="%s"> </ul> </div>', i + 1, i + 1, "course-group-" + (i + 1)));
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
        data: JSON.stringify({group: groupId, user: "temp"}),
        success: function (data) {
            var courses = data.data;
            for (i = 0; i < courses.length; i++) {
                var check = "";
                if (courses[i].isPassed) {
                    check = "checked";
                }
                $("#course-group-" + groupId).append(sprintf('<li><input type="checkbox" name="chk" id="%s" %s>%s</input></li>', courses[i].id, check, courses[i].name));
                $("#course-group-" + groupId + " li:last").data('course', courses[i]);
            }
        },
    });


}
