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
