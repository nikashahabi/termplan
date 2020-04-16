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
