from django.urls import path
from src.views import list_course, login, signup

urlpatterns = [
    path('courses_list', list_course),
    path('login', login),
    path('signup', signup)

]
