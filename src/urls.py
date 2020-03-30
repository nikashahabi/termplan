from django.urls import re_path

from src.views import list_course, add_course, delete_course

urlpatterns = [
    re_path(r'^courses_list/?$', list_course),
    re_path(r'^add_course/?$', add_course),
    re_path(r'^delete_course/?$', delete_course)
]
