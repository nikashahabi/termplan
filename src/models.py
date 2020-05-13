from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class ChartTable(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    code = models.IntegerField(blank=True, null=True)
    dep = models.ForeignKey(Department, on_delete=models.CASCADE)
    req_passed_units = models.IntegerField(blank=True, null=True)
    req_not_stared_units = models.IntegerField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"dep: {self.dep} - table{self.code} : {self.name}"


class Professor(models.Model):
    name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"professor: {self.name} - dep:{self.department.name}"


class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=256)
    unit = models.IntegerField(null=True, blank=True)
    code = models.IntegerField(unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default="MCS")
    table = models.ForeignKey(ChartTable, on_delete=models.CASCADE, null=True)
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return f"course:{self.name} - dep:{self.department}"


class SemesterCourse(models.Model):
    semester = models.CharField(max_length=256, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.FloatField(null=True, blank=True)
    end_time = models.FloatField(null=True, blank=True)
    day1 = models.CharField(max_length=256, null=True, blank=True)
    day2 = models.CharField(max_length=256, null=True, blank=True)
    exam = models.DateTimeField(null=True, blank=True)
    ta_day = models.CharField(max_length=256, null=True, blank=True)
    ta_time = models.TimeField(null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    group = models.IntegerField(default=1)
    info = models.TextField(null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"course:{self.course.name} - semester:{self.semester}"


class UserSchedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(SemesterCourse)
    semester = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"user:{self.user.username} - semester:{self.semester}"


class UserPassed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.ManyToManyField(Course)
    units = models.IntegerField(default=0)

    def __str__(self):
        return f"user: {self.user.username} - units: {self.units}"
