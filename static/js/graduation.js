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
           $("#course-group-" + groupId).append(sprintf('<li><input type="checkbox" name="chk" id="%s">%s</input></li>', courses[i].id, courses[i].name));
           $("#course-group-" + groupId + " li:last").data('course', courses[i]);
           }
           },
           });
    
    
}
