from django.contrib import admin
from .models import AttendanceSession, Attendance

# Register your models here once
admin.site.register(AttendanceSession)
admin.site.register(Attendance)