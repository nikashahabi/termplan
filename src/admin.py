from django.contrib import admin

# Register your models here.
from src.models import Department, Professor, User, Courses

admin.site.register(Department)
admin.site.register(Professor)
admin.site.register(User)
admin.site.register(Courses)
