from django.urls import path
from src.views import list_course
urlpatterns = [
    path('courses_list', list_course)
]
