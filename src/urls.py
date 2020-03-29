from django.urls import path

from src.views import list_course, add_course, course_delete

urlpatterns = [
    path('courses_list', list_course),
    path('add_course', add_course),
    path('del_course', course_delete)
]
