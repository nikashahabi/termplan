import json

from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from src.excel_handler import handle_uploaded_semester_file, handle_uploaded_chart_table_file, \
    handle_uploaded_chart_courses_file
from src.forms import LoginForm
from src.models import SemesterCourse, UserSchedule, Department, Course, UserPassed, ChartTable, User


def log_out(req):
    logout(req)
    return redirect("/login/")


@csrf_exempt
def log_in(request):
    user_name = request.POST.get('username', None)
    pass_word = request.POST.get('password', None)
    print(user_name)
    print(pass_word)
    if user_name is None or pass_word is None:
        login_form = LoginForm()
        message = ""
    else:
        user = auth.authenticate(username=user_name, password=pass_word)
        if user is not None:
            print("user is not none")
            login(request, user)
            return redirect('src:home')
        else:
            message = 'نام کاربری یا رمز عبور اشتباه است!'
            login_form = LoginForm(request.POST)

    return render(request, "login.html", {
        'message': message,
        'login_form': login_form
    })


def sign_up(request):
    form = LoginForm(request.POST)
    if form.is_valid():
        user = form.save()
        user.set_password(user.password)
        user.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('src:home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'login_form': form})


@login_required(login_url='/login/')
def homepage(request):
    username = request.user.username
    return render(request, 'homepage.html', {'username': username})


@csrf_exempt
def courses_list(request):
    user = request.user
    print(request.body)
    data = json.loads(request.body)
    print(data)
    department_id = data.get("dep_id", None)
    courses = []
    data_of_db = SemesterCourse.objects.filter(course__department_id=department_id)
    for data in data_of_db:
        if not is_passed(user, data.course):
            days = [data.day1, data.day2]
            courses.append({
                "course_id": f"{data.course.code}-{data.group}",
                "name": data.course.name,
                "class_times": [{
                    "day": day,
                    "start": data.start_time,
                    "end": data.end_time
                } for day in days if day],
                "ta_time": data.ta_time,
                "ta_day": data.ta_day,
                "exam_time": data.exam,
                "department": data.course.department.name,
                "units": data.course.unit,
                "instructor": data.professor.name,
                "course_number": data.course.code,
                "info": data.info,
                "capacity": data.capacity

            })
    return JsonResponse({"data": courses})


@csrf_exempt
def add_course(request):
    user = request.user
    data = json.loads(request.body)
    course_id = data.get("course_id")
    course_code, course_group = course_id.split("-")
    print(course_code, course_group)
    selected_course = SemesterCourse.objects.filter(course__code=course_code, group=course_group).first()
    user_semester, _ = UserSchedule.objects.get_or_create(user=user)
    # overlapping_course = user_semester.courses.filter(Q(day1=wanted_course.day1) | Q(day2=wanted_course.day2), Q(
    #     start_time__range=(wanted_course.start_time, wanted_course.end_time)) | Q(
    #     end_time__range=(wanted_course.start_time, wanted_course.end_time))).exclude(
    #     Q(start_time=wanted_course.end_time) | Q(end_time=wanted_course.start_time))
    # if overlapping_course.exists():
    #     return JsonResponse({
    #         "error": "تداخل دارد",
    #         "overlapping course": overlapping_course.first().course.name
    #     })
    user_semester.courses.add(selected_course)
    return JsonResponse({"message": "با موفقیت اضاقه شد"})


@csrf_exempt
def delete_course(request):
    data = json.loads(request.body)
    course_id = data.get("course_id")
    user = request.user
    course_code, course_group = course_id.split("-")
    selected_course = SemesterCourse.objects.filter(course__code=course_code, group=course_group, ).first()
    user_semester, _ = UserSchedule.objects.get_or_create(user=user)
    if selected_course in user_semester.courses.all():
        user_semester.courses.remove(selected_course)
        return JsonResponse({"message": "با موفقیت حذف شد"})
    else:
        return JsonResponse({"message": "درس مورد نظر یافت نشد"})


@login_required(login_url='/login/')
def schedule(request):
    user = request.user
    departments = []
    for dep in Department.objects.all():
        departments.append({"name": dep.name, "id": dep.id})
    data = {
        "username": user.username,
        "departments": departments
    }
    return render(request, 'grid.html', data)


@login_required(login_url='/login/')
@csrf_exempt
def graduation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        table_no = data.get("group")
        user = request.user
        department = User.objects.filter(username=user.username).first().department
        if table_no == "0" or table_no == 0:
            table_count = ChartTable.objects.filter(dep=department).count()
            return JsonResponse({"group_count": table_count})
        user_passed_courses = UserPassed.objects.filter(user=user)
        table_courses = Course.objects.filter(table__code=table_no, department=department)
        course_list = []
        for course in table_courses:
            course_list.append({
                "id": course.code,
                "name": course.name,
                "is_starred": course.is_starred,
                "is_passed": is_passed(user, course)
            })
        table = ChartTable.objects.filter(code=table_no, dep=department).first()
        return JsonResponse({"user_courses": course_list, "info": table.info})
    return render(request, 'graduation.html', {"username": request.user})


@csrf_exempt
def add_passed_course(request):
    data = json.loads(request.body)
    courses = data.get("passed_courses")
    user = request.user
    if_exist = UserPassed.objects.filter(user=user).count()
    if if_exist:
        UserPassed.objects.filter(user=user).delete()
    user_passed, _ = UserPassed.objects.get_or_create(user=user)
    for crs in courses:
        course = Course.objects.filter(code=crs).first()
        if course not in user_passed.courses.all():
            user_passed.courses.add(course)
            passed_units = user_passed.units
            user_passed.units = passed_units + course.unit
            user_passed.save()
    return JsonResponse({})


@csrf_exempt
def show_remained(request):
    data = json.loads(request.body)
    table_number = data.get("table_num")
    user = request.user
    department = User.objects.filter(username=user.username).first().department
    all_courses = Course.objects.filter(department=department, table=table_number)
    user_passed_courses = UserPassed.objects.filter(user=user, courses__table__code=table_number)
    remained = []
    passed_unit = 0
    for course in all_courses:
        if course.is_starred and not is_passed(user, course):
            remained.append({"course_name": course.name,
                             "course_id": course.code,
                             "course_unit": course.unit,
                             "necessity": True})
    if user_passed_courses.exists():
        for user_course in user_passed_courses.first().courses.all():
            if not user_course.is_starred:
                passed_unit += user_course.unit
    chart = ChartTable.objects.filter(dep=department, code=table_number).first()
    optional_remained = chart.req_not_stared_units - passed_unit
    table_courses = Course.objects.filter(table__code=table_number, department=department)
    course_list = []
    for course in table_courses:
        course_list.append({
            "course_id": course.code,
            "course_name": course.name,
            "is_passed": is_passed(user, course)
        })
    all_passed = UserPassed.objects.filter(user=user).first()
    return JsonResponse({
        "username": user.username,
        "remain": remained,
        "optional_remained": optional_remained if optional_remained > 0 else 0,
        "chart_course": course_list,
        "all_passed": all_passed.units if all_passed else 0
    })


def is_passed(user, course):
    user_passed_courses = UserPassed.objects.filter(user=user)
    if not user_passed_courses.exists():
        return False
    if course in user_passed_courses.first().courses.all():
        return True
    return False


class SemesterCourseAddView(APIView):

    def post(self, request):
        success = handle_uploaded_semester_file(request.FILES['semester_file'])
        return render(request, 'semester_course_add.html', {"success": success})

    def get(self, request):
        return render(request, 'semester_course_add.html', {"message": "فایل را ارسال کنید"})


class ChartTableAddView(APIView):

    def post(self, request):
        success = handle_uploaded_chart_table_file(request.FILES['department_file'])
        return render(request, 'department_chart_add.html', {"success": success})

    def get(self, request):
        return render(request, 'department_chart_add.html', {"message": "فایل را ارسال کنید"})


class ChartCourseAddView(APIView):

    def post(self, request):
        success = handle_uploaded_chart_courses_file(request.FILES['course_file'])
        return render(request, 'add_chart_course.html', {"success": success})

    def get(self, request):
        return render(request, 'add_chart_course.html', {"message": "فایل را ارسال کنید"})
