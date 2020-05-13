from django.urls import re_path

from src.views import courses_list, add_course, delete_course, schedule, graduation, add_passed_course, show_remained

urlpatterns = [
    re_path(r'^courses_list/?$', courses_list),
    re_path(r'^add_course/?$', add_course),
    re_path(r'^delete_course/?$', delete_course),
    re_path(r'^schedule/?$', schedule),
    re_path(r'^graduation/?$', graduation),
    re_path(r'^add_passed_course/?$', add_passed_course),
    re_path(r'^remained_courses/?$', show_remained)
    # re_path(r'^course_chart/', course_chart)

]
