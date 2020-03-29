import json

from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from src.models import SemesterCourse, User, UserCourse


@csrf_exempt
def list_course(request):
    data = json.loads(request.body)
    department = data.get("department")
    semester = data.get("semester")
    courses = []
    data_of_db = SemesterCourse.objects.filter(semester__exact=semester, course__department__name=department)
    for data in data_of_db:
        courses.append({
            "name": data.course.name,
            "start_time": data.start_time,
            "end_time": data.end_time,
            "day1": data.Day1,
            "day2": data.Day2,
            "ta_time": data.ta_time,
            "ta_day": data.ta_day,
            "exam": data.exam,
            "department": data.course.department.name,
            "unit": data.course.unit,
            "prof": data.professor.name,
            "semester": data.semester

        })
    return JsonResponse({"data": courses})


@csrf_exempt
def add_course(request):
    data = json.loads(request.body)
    username = data.get("username")
    user = User.objects.filter(username=username).first()
    course_name = data.get("course")
    semester = data.get("semester")
    wanted_course = SemesterCourse.objects.filter(course__name=course_name, semester=semester).first()
    user_semester, _ = UserCourse.objects.get_or_create(user=user, semester=semester)
    overlapping_course = user_semester.courses.filter(Q(day1=wanted_course.day1) | Q(day2=wanted_course.day2), Q(
        start_time__range=(wanted_course.start_time, wanted_course.end_time)) | Q(
        end_time__range=(wanted_course.start_time, wanted_course.end_time))).exclude(
        Q(start_time=wanted_course.end_time) | Q(end_time=wanted_course.start_time))
    if overlapping_course.exists():
        return JsonResponse({
            "error": "تداخل دارد",
            "overlapping course": overlapping_course.first().course.name
        })
    user_semester.courses.add(wanted_course)
    return JsonResponse({"message": "با موفقیت اضاقه شد"})


@csrf_exempt
def course_delete(request):
    data = json.loads(request.body)
    username = data.get("username")
    user = User.objects.filter(username=username).first()
    semester = data.get("semester")
    course_name = data.get("course")
    selected_course = SemesterCourse.objects.filter(course__name=course_name, semester=semester).first()
    user_semester, _ = UserCourse.objects.get_or_create(user=user, semester=semester)
    if user_semester.courses.filter(course=selected_course).exists():
        user_semester.courses.remove(selected_course)
        return JsonResponse({"message": "با موفقیت حذف شد"})
    else:
        return JsonResponse({"message": "درس مورد نظر یافت نشد"})
