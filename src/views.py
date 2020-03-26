import json

from django.http import JsonResponse
from django.shortcuts import render

from src.models import Courses


def list_course(request):
    data = json.loads(request.body)
    department = data.get("department")
    term = data.get("term")
    courses = []
    data_of_db = Courses.objects.filter(semester=term, department=department)
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
            "department": data.department,
            "unit": data.unit,
            "prof": data.professor,
            "semester": data.term

        })
        return JsonResponse({"data": courses})
