from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def is_professor(user):
    return user.groups.filter(name='Professors').exists()

def is_student(user):
    return user.groups.filter(name='Students').exists()


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from .models import AttendanceSession, Attendance

@login_required
@user_passes_test(is_professor)
def professor_dashboard(request):
    sessions = AttendanceSession.objects.filter(created_by=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        AttendanceSession.objects.create(title=title, created_by=request.user)
        return redirect('professor_dashboard')
        
    return render(request, 'main/professor_dashboard.html', {'sessions': sessions})

@login_required
@user_passes_test(is_student)
def student_dashboard(request):
    active_sessions = AttendanceSession.objects.filter(is_active=True)
    
    # Get IDs of sessions the student has already checked into
    checked_in_session_ids = Attendance.objects.filter(
        student=request.user
    ).values_list('session_id', flat=True)
    
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        session = get_object_or_404(AttendanceSession, id=session_id, is_active=True)
        
        # Create attendance record if not already checked in
        Attendance.objects.get_or_create(session=session, student=request.user)
        return redirect('student_dashboard')

    context = {
        'active_sessions': active_sessions,
        'checked_in_session_ids': checked_in_session_ids,
    }
    return render(request, 'main/student_dashboard.html', context)