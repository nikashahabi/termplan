from django.urls import path
from src.views import list_course, login

urlpatterns = [
    path('courses_list', list_course),
    path('login', login)
]
