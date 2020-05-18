import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from src.models import SemesterCourse, User, UserSchedule, Department, Course, UserPassed, ChartTable

from terminator.src.excel_handeler import handle_uploaded_file


@csrf_exempt
def courses_list(request):
    data = json.loads(request.body)
    department_id = data.get("dep_id")
    semester = data.get("semester")
    courses = []
    data_of_db = SemesterCourse.objects.filter(semester__exact=semester, course__department_id=department_id)
    for data in data_of_db:
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
            "semester": data.semester,
            "course_number": data.course.code,
            "info": data.info,
            "capacity": data.capacity

        })
    return JsonResponse({"data": courses})


@csrf_exempt
def add_course(request):
    data = json.loads(request.body)
    # username = data.get("username")
    user = User.objects.filter(username="temp").first()
    course_id = data.get("course_id")
    course_code, course_group = course_id.split("-")
    print(course_code, course_group)
    semester = data.get("semester")
    selected_course = SemesterCourse.objects.filter(course__code=course_code, group=course_group,
                                                    semester=semester).first()
    user_semester, _ = UserSchedule.objects.get_or_create(user=user, semester=semester)
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
    # username = data.get("username")
    semester = data.get("semester")
    course_id = data.get("course_id")
    user = User.objects.filter(username="temp").first()  # temp user for now
    course_code, course_group = course_id.split("-")
    selected_course = SemesterCourse.objects.filter(course__code=course_code, group=course_group,
                                                    semester=semester).first()
    user_semester, _ = UserSchedule.objects.get_or_create(user=user, semester=semester)
    if selected_course in user_semester.courses.all():
        user_semester.courses.remove(selected_course)
        return JsonResponse({"message": "با موفقیت حذف شد"})
    else:
        return JsonResponse({"message": "درس مورد نظر یافت نشد"})


def schedule(request):
    temp_user, _ = User.objects.get_or_create(username="temp")  # temp user for now
    departments = []
    for dep in Department.objects.all():
        departments.append({"name": dep.name, "id": dep.id})
    data = {
        "username": temp_user.username,
        "departments": departments
    }
    return render(request, 'grid.html', data)


@csrf_exempt
def graduation(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("user")
        table_no = data.get("group")
        user = User.objects.filter(username=username).first()
        department = user.department
        if table_no == 0:
            table_count = ChartTable.objects.filter(department=department).count()
            return render(request, 'grid.html', {"group_count": table_count})
        user_passed_courses = UserPassed.objects.filter(user=user, courses__table__code=table_no).first()
        table_courses = Course.objects.filter(table__code=table_no, department=user.department)
        course_list = []
        for course in table_courses:
            course_list.append({
                "course_id": course.code,
                "course_name": course.name,
                "is_passed": True if course in user_passed_courses.courses.all() else False
            })
        return render(request, 'graduation.html', {"user_courses": course_list})
    return render(request, 'graduation.html')


@csrf_exempt
def add_passed_course(request):
    data = json.loads(request.body)
    username = data.get("username")
    courses = data.get("courses")
    user = User.objects.filter(username=username).first()
    user_passed, _ = UserPassed.objects.get_or_create(user=user)
    for crs in courses:
        course = Course.objects.filter(code=crs.get("code")).first()
        if course not in user_passed.courses.all():
            user_passed.courses.add(course)
            passed_units = user_passed.units
            user_passed.units = passed_units + course.unit
            user_passed.save()
    return JsonResponse({})


@csrf_exempt
def show_remained(request):
    data = json.loads(request.body)
    username = data.get("username")
    table_number = data.get("table_num")
    user = User.objects.filter(username=username).first()
    department = user.department
    all_courses = Course.objects.filter(department=department, table=table_number)
    user_passed_courses = UserPassed.objects.filter(user=user, courses__table__code=table_number).first()
    remained = []
    passed_unit = 0
    for course in all_courses:
        if course.is_starred and course not in user_passed_courses.courses.all():
            remained.append({"course_name": course.name,
                             "course_id": course.code,
                             "course_unit": course.unit,
                             "necessity": True})
    for user_course in user_passed_courses.courses.all():
        if not user_course.is_starred:
            passed_unit += user_course.unit
    chart = ChartTable.objects.filter(department=department, code=table_number).first()
    optional_remained = chart.req_not_stared_units - passed_unit
    # chart_table = ChartTable.objects.filter(dep=department, code=table_number).first()
    # if passed_unit <= chart_table.req_passed_units:
    #     for user_course in user_passed_courses.courses.all():
    #         if not user_course.is_starred:
    #             remained.append({"course_name": user_course.course.department,
    #                              "necessity": False})
    user_passed_courses = UserPassed.objects.filter(user=user, courses__table__code=table_number).first()
    table_courses = Course.objects.filter(table__code=table_number, department=department)
    course_list = []
    for course in table_courses:
        course_list.append({
            "course_id": course.code,
            "course_name": course.name,
            "is_passed": True if course in user_passed_courses.courses.all() else False
        })
    return render(request, 'graduation.html', {
        "username": username,
        "remain": remained,
        "optional_remained": optional_remained,
        "chart_course": course_list
    })


class SemesterCourseAddView(ListView):
    model = SemesterCourse
    template_name = 'semester_course_add.html'

    def post(self, request):
        try:
            handle_uploaded_file(request, request.FILES['semester_file'])
            success = True
        except:
            success = False
        return render(request, 'semester_course_add.html', {"success": success})
