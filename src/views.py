import json

from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from src.forms import SignUpForm
from src.models import Courses


@csrf_exempt
def list_course(request):
    data = json.loads(request.body)
    department = data.get("department")
    semester = data.get("term")
    courses = []
    data_of_db = Courses.objects.filter(semester__exact=semester, department__name=department)
    for data in data_of_db:
        courses.append({
            "name": data.name,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "day1": data.Day1,
            "day2": data.Day2,
            "ta_time": data.ta_time,
            "ta_day": data.ta_day,
            "exam": data.exam,
            "department": data.department.name,
            "unit": data.unit,
            "prof": data.professor.name,
            "semester": data.semester

        })
        return JsonResponse({"data": courses})


def login(request):
    if request.method == 'GET':
        return render(request, 'auth/../templates/login.html')
    elif request.method == 'POST':
        user_name = request.POST['username']
        pass_word = request.POST['password']
        user = auth.authenticate(username=user_name, password=pass_word)
        if user is None:
            return render(request, 'auth/../templates/login.html', {'Error': 'Wrong user name or password'})
        else:
            auth.login(request, user)
            return redirect('course_list')


def signup(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
