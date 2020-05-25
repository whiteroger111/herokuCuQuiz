from django.contrib import admin
from django.urls import path, include
from classroom.views import classroom, students, teachers

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('classroom.urls')),
    path('accounts/', students.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', students.CustomLogoutView.as_view(), name='logout'),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
