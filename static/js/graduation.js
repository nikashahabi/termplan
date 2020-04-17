var get_courses = new Array();
function reply_click(clicked_id){
    
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
function submit_button(){
    var courses = new Array();
    var index = 0;
    $("input:checkbox[name=chk]:checked").each(function () {
                                               courses[index] = $(this).attr("id");
                                               index++;
                                               });
    $.ajax({
           url: '/passed_course',
           type: 'post',
           data: JSON.stringify({ passed_courses: courses}),
           success: function(data) {
           }
           });
    
}
function add_course(groupId){
    for(var u in get_courses) {
        if(u == groupId)
            return;
    }
    get_courses[groupId] = groupId;
    $.ajax({
           url: '/courses_list_group',
           type: 'post',
           data: { group: groupId},
           success: function(data){
           var courses = data.data;
           for(i = 0; i < courses.length; i++) {
           var checked = "unchecked";
           if(courses[i].isPassed == true){
           checked = "checked";
           }
           $("#course-group-" + groupId).append(sprintf('<li><input type="checkbox" name="chk" id="%s" %s>%s</input></li>', courses[i].id, checked, courses[i].name));
           $("#course-group-" + groupId + " li:last").data('course', courses[i]);
           }
           },
           });
    
    
}
