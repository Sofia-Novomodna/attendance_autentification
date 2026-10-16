from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class AttendanceSession(models.Model):
    title = models.CharField(max_length=100) # e.g., "Math 101 - Lecture 1"
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) # Turn off when attendance closes
    created_by = models.ForeignKey(User, on_delete=models.CASCADE) # Professor

    def __str__(self):
        return f"{self.title} ({self.created_at.date()})"

class Attendance(models.Model):
    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        # Ensures a student can only check in once per session
        unique_together = ('session', 'student')

    def __str__(self):
        return f"{self.student.username} - {self.session.title}"