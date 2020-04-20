from django.urls import re_path

from src.views import courses_list, add_course, delete_course, schedule

urlpatterns = [
    re_path(r'^courses_list/?$', courses_list),
    re_path(r'^add_course/?$', add_course),
    re_path(r'^delete_course/?$', delete_course),
    re_path(r'^schedule/', schedule)
]
