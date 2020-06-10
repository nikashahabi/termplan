from django.contrib import admin

# Register your models here.
from src.models import Department, Professor, User, Course, SemesterCourse, UserSchedule, UserPassed, ChartTable

admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(User)
admin.site.register(Course)
admin.site.register(SemesterCourse)
admin.site.register(UserSchedule)
admin.site.register(UserPassed)
admin.site.register(ChartTable)
