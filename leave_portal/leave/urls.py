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

from django.urls import path, include
from .views import students, faculty, staff, hod, leaves, dppc

urlpatterns = [
    path('', leaves.home, name='home'),

    path('students/', include(([
                                path('dash_board', students.stud_dash_board, name='stud_dash_board'),
                                path('stud_profile', students.stud_profile, name='stud_profile'),
                                path('edit_profile/<pk>/', students.EditUserProfileView.as_view(),
                                        name='edit_profile'),
                                path('apply_leave/', students.ApplyLeave1, name='applyleave'),
                                path('apply_leave_status/', students.CurrentStatus, name='CurrStatus'),
                                path('leave_history/', students.History, name='history'),
                                path('leave_comments/', students.ShowComments, name='ShowComments'),
                                path('leave_past_comments/<pk>/', students.PastComments, name='PastComment'),
                                path('my_profile/', students.MyProfile, name='my_profile'),

                               ], 'leave'), namespace='students')),

    path('faculty/', include(([
                                path('dash_board', faculty.faculty_dash_board, name='fac_dash_board'),
                                path('fac_profile', faculty.fac_profile, name='fac_profile'),
                                path('edit_profile/<pk>/', faculty.EditUserProfileView.as_view(),
                                       name='edit_profile'),
                                path('TA_leave_request', faculty.TALeaveRequest, name='ta_request'),
                                path('Supervisor_leave_request', faculty.SupervisorLeaveRequest,
                                       name='supervisor_request'),
                                path('TA_leave_approve/<pk>/', faculty.TALeaveRequestApprove, name='ta_approve'),
                                path('SV_leave_approve/<pk>/', faculty.SVLeaveRequestApprove, name='sv_approve'),
                                path('TA_leave_cancel/<pk>/', faculty.TALeaveRequestCancel, name='ta_cancel'),
                                path('SV_leave_cancel/<pk>/', faculty.SVLeaveRequestCancel, name='sv_cancel'),
                                path('TA_leave_history', faculty.TALeaveHistory, name='ta_history'),
                                path('SV_leave_history', faculty.SVLeaveHistory, name='sv_history'),
                                path('TA_leave_comment/<pk>/', faculty.SaveComments, name='ta_comment'),

                              ], 'leave'), namespace='faculty')),

    path('staff/', include(([
                                path('dash_board', staff.staff_dash_board, name='staff_dash_board'),
                                path('staff_profile', staff.staff_profile, name='staff_profile'),
                                path('edit_profile/<pk>/', staff.EditUserProfileView.as_view(), name='edit_profile'),
                                path('staff_leave_request', staff.AllLeaveRequest, name='leave_request'),
                                path('staff_All_leave_approve/<pk>/', staff.AllLeaveRequestApprove, name='staff_approve'),
                                path('staff_All_leave_cancel/<pk>/', staff.AllLeaveRequestCancel, name='staff_cancel'),
                                path('staff_All_leave_history', staff.AllLeaveHistory, name='leave_history'),
                                path('Staff_leave_comment/<pk>/', staff.SaveComments, name='staff_comment'),
                                path('mtech_list', staff.ShowMtechList, name='MtechList'),
                                path('phd_list', staff.ShowPhdList, name='PhdList'),
                                path('reset_odinary_leaves', staff.ResetOdinaryLeaves, name='UpdateOdinary'),
                                path('reset_other_leaves', staff.ResetAcademicAndMedicalLeaves, name='UpdateLeaves'),
                            ], 'leave'), namespace='staff')),

    path('hod/', include(([
                                path('dash_board', hod.hod_dash_board, name='hod_dash_board'),
                                path('hod_profile', hod.hod_profile, name='hod_profile'),
                                path('edit_profile/<pk>/', hod.EditUserProfileView.as_view(), name='edit_profile'),
                                path('hod_leave_request', hod.AllLeaveRequest, name='leave_request'),
                                path('hod_All_leave_approve/<pk>/', hod.AllLeaveRequestApprove, name='hod_approve'),
                                path('hod_All_leave_cancel/<pk>/', hod.AllLeaveRequestCancel, name='hod_cancel'),
                                path('hod_All_leave_history', hod.AllLeaveHistory, name='leave_history'),
                                path('Hod_leave_comment/<pk>/', hod.SaveComments, name='hod_comment'),


                          ], 'leave'), namespace='hod')),
    path('dppc/', include(([
                                path('dash_board', dppc.dppc_dash_board, name='dppc_dash_board'),
                                path('dppc_profile', dppc.dppc_profile, name='dppc_profile'),
                                path('edit_profile/<pk>/', dppc.EditUserProfileView.as_view(), name='edit_profile'),
                                path('dppc_leave_request', dppc.AllLeaveRequest, name='leave_request'),
                                path('dppc_All_leave_approve/<pk>/', dppc.AllLeaveRequestApprove, name='dppc_approve'),
                                path('dppc_All_leave_cancel/<pk>/', dppc.AllLeaveRequestCancel, name='dppc_cancel'),
                                path('dppc_All_leave_history', dppc.AllLeaveHistory, name='leave_history'),
                                path('dppc_leave_comment/<pk>/', dppc.SaveComments, name='dppc_comment'),

                          ], 'leave'), namespace='dppc')),

]
