"""leave_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from leave.views import leaves, students, faculty, staff, hod, dppc
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('leave.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', leaves.SignUpView.as_view(), name='signup'),
    # path('accounts/login/', leaves.LogInView.as_view(), name='login'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/faculty/', faculty.FacultySignUpView.as_view(), name='faculty_signup'),
    path('accounts/signup/staff/', staff.StaffSignUpView.as_view(), name='staff_signup'),
    path('accounts/signup/hod/', hod.HodSignUpView.as_view(), name='hod_signup'),
    path('accounts/signup/dppc/', dppc.DppcSignUpView.as_view(), name='dppc_signup'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)


# handler404 = leaves.handler404
# handler500 = leaves.handler500
