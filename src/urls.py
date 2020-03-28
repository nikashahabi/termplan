from django.urls import path

from src.views import list_course, add_course

urlpatterns = [
    path('courses_list', list_course),
    path('add_course', add_course)
]
