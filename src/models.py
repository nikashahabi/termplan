from django.contrib.auth.models import AbstractUser
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Professor(models.Model):
    name = models.CharField(max_length=128)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f"professor: {self.name} - dep:{self.department}"


class User(AbstractUser):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)


class Course(models.Model):
    name = models.CharField(max_length=256)
    unit = models.IntegerField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default="MCS")

    def __str__(self):
        return f"course:{self.name} - dep:{self.department}"


class SemesterCourse(models.Model):
    semester = models.CharField(max_length=256, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    Day1 = models.CharField(max_length=256, null=True, blank=True)
    Day2 = models.CharField(max_length=256, null=True, blank=True)
    exam = models.DateTimeField(null=True, blank=True)
    ta_day = models.CharField(max_length=256, null=True, blank=True)
    ta_time = models.TimeField(null=True, blank=True)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, null=True, blank=True)
    group = models.IntegerField(default=1)

    def __str__(self):
        return f"course:{self.course.name} - semester:{self.semester}"


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ManyToManyField(SemesterCourse)
    semester = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return f"user:{self.user.username} - semester:{self.semester}"
