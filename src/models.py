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


class Courses(models.Model):
    name: models.CharField(max_length=256)
    start_time: models.TimeField(null=True, blank=True)
    end_time: models.TimeField(null=True, blank=True)
    Day1: models.CharField(max_length=256, null=True, blank=True)
    Day2: models.CharField(max_length=256, null=True, blank=True)
    unit: models.IntegerField(null=True, blank=True)
    exam: models.CharField(max_length=256, null=True, blank=True)
    ta_day: models.CharField(max_length=256, null=True, blank=True)
    ta_time: models.TimeField(null=True, blank=True)
    semester: models.CharField(max_length=256, null=True, blank=True)
    department: models.ForeignKey(Department, on_delete=models.CASCADE)
    professor:  models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"course:{self.name} - dep:{self.department}"