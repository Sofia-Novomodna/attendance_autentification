from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('professor/', views.professor_dashboard, name='professor_dashboard'),
]