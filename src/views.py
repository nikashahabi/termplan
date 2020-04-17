import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from src.models import SemesterCourse, User, UserCourse, Department, Course


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
    user_semester, _ = UserCourse.objects.get_or_create(user=user, semester=semester)
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
    user_semester, _ = UserCourse.objects.get_or_create(user=user, semester=semester)
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


def course_chart(request):
    data = json.loads(request.body)
    department = data.get("department")
    all_course = Course.objects.get(department=department)
    list_course = []
    for course in all_course:
        list_course[course.chart].append(course)
    return render(request, 'graduation.html', list_course)

# def show_remained(request):
#     data = json.loads(request.body)
#     username = data.get("username")
#     department = data.get("department")
#     passed_courses=data.get()
#     remained = []
#     user_passed, _ = UserCourse.objects.get_or_create(user=username)
#     all_course=Course.objects.get(department=department)
#     for i in many_chart(department):
#         for courses in all_course:
#             if courses not in user_passed:
#                if courses.isStared:
#
#                 else
