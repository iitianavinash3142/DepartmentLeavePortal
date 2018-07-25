from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, UpdateView)

from ..forms import FacultySignUpForm, FacultyProfileInfoForm, FacultyProfileUpdateForm, CommentForm
from ..models import User, Faculty, ApplyLeave, Student, Comments
from django.urls import reverse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import faculty_required
from django.db.models import Q


class FacultySignUpView(CreateView):
    model = User
    form_class = FacultySignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'faculty'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('faculty:fac_profile')


@login_required
@faculty_required
def faculty_dash_board(request):
    # for count leave request
    TaStudent = Student.objects.all().filter(TA_instructor=request.user)
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=TaStudent)).count()
    SvStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=SvStudent)).count()
    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=SvStudent)).order_by('-pk').count()
    TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=TaStudent)).order_by('-pk').count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/faculty_dashboard.html', {'user_obj': user_obj,
                                                                  'TaLength': TaLength,
                                                                  'SvLength': SvLength,
                                                                  'TaHistory': TaHistory,
                                                                  'SvHistory': SvHistory,
                                                                  })
    except:
        return redirect('faculty:fac_profile')


@login_required
@faculty_required
def fac_profile(request):
    save = False
    if request.method == "POST":
        profile_form = FacultyProfileInfoForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            profile.user = request.user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            save = True
        else:
            print(profile_form.errors)
    else:

        profile_form = FacultyProfileInfoForm()
    # for count leave request
    TaStudent = Student.objects.all().filter(TA_instructor=request.user)
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=TaStudent)).count()
    SvStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=SvStudent)).count()
    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=SvStudent)).order_by('-pk').count()
    TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=TaStudent)).order_by('-pk').count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/faculty_dashboard.html', {'user_obj': user_obj,
                                                            'profile_form': profile_form,
                                                            'save': save,
                                                            'TaLength': TaLength,
                                                            'SvLength': SvLength,
                                                            'TaHistory': TaHistory,
                                                            'SvHistory': SvHistory,
                                                            })
    except:
        return render(request, 'faculty/fac_profile.html', {'profile_form': profile_form,
                                                            'save': save,
                                                            'TaLength': TaLength,
                                                            'SvLength': SvLength,
                                                            'TaHistory': TaHistory,
                                                            'SvHistory': SvHistory,
                                                            })


@method_decorator([login_required, faculty_required], name='dispatch')
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = Faculty
    form_class = FacultyProfileUpdateForm
    template_name = "faculty/edit_profile.html"

    def get_context_data(self, **kwargs):
        user2 = get_object_or_404(User, pk=self.kwargs['pk'])
        user_obj = Faculty.objects.get(user=user2)
        # for count leave request
        TaStudent = Student.objects.all().filter(TA_instructor=user2)
        TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=TaStudent)).count()
        SvStudent = Student.objects.all().filter(Q(Supervisor_1=user2))
        SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=SvStudent)).count()
        # for count leave history
        SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=SvStudent)).order_by('-pk').count()
        TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=TaStudent)).order_by('-pk').count()
        kwargs['user_obj'] = user_obj
        kwargs['TaLength'] = TaLength
        kwargs['SvLength'] = SvLength
        kwargs['TaHistory'] = TaHistory
        kwargs['SvHistory'] = SvHistory
        return super().get_context_data(**kwargs)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.facultys

    def get_success_url(self, *args, **kwargs):
        return reverse("faculty:fac_dash_board")


@login_required
@faculty_required
def TALeaveRequest(request):
    # for main function queryset
    TaStudent = Student.objects.all().filter(TA_instructor=request.user)
    LeaveAppliedStudent = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=TaStudent))

    # for count leave request
    FacultyStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=FacultyStudent)).count()
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=TaStudent)).count()

    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=FacultyStudent)).order_by('-pk').count()
    TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=TaStudent)).order_by('-pk').count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/ta_leaverequest.html', {'user_obj': user_obj,
                                                                'leaverequest': LeaveAppliedStudent,
                                                                'TaLength': TaLength,
                                                                'SvLength': SvLength,
                                                                'TaHistory': TaHistory,
                                                                'SvHistory': SvHistory,
                                                                })
    except:
        return render(request, 'faculty/ta_leaverequest.html', {'leaverequest': LeaveAppliedStudent,
                                                                'TaLength': TaLength,
                                                                'SvLength': SvLength,
                                                                'TaHistory': TaHistory,
                                                                'SvHistory': SvHistory,
                                                                })


@login_required
@faculty_required
def SupervisorLeaveRequest(request):
    # for main function
    SvStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    LeaveAppliedStudent = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=SvStudent))

    # for count leave request
    FacultyStudent = Student.objects.all().filter(TA_instructor=request.user)
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=SvStudent)).count()
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=FacultyStudent)).count()

    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=SvStudent)).order_by('-pk').count()
    TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=FacultyStudent)).order_by('-pk').count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/super_leaverequest.html', {'user_obj': user_obj,
                                                                   'leaverequest': LeaveAppliedStudent,
                                                                   'TaLength': TaLength,
                                                                   'SvLength': SvLength,
                                                                   'TaHistory': TaHistory,
                                                                   'SvHistory': SvHistory,
                                                                   })
    except:
        return render(request, 'faculty/super_leaverequest.html', {'leaverequest': LeaveAppliedStudent,
                                                                   'TaLength': TaLength,
                                                                   'SvLength': SvLength,
                                                                   'TaHistory': TaHistory,
                                                                   'SvHistory': SvHistory,
                                                                   })


@login_required
@faculty_required
def TALeaveRequestApprove(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    if '1' not in leave.SentTo:
        leave.Flag = 3
    else:
        leave.Flag = 2
    leave.save()

    return redirect("faculty:ta_request")


@login_required
@faculty_required
def TALeaveRequestCancel(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 11
    leave.save()

    return redirect("faculty:ta_request")


@login_required
@faculty_required
def SVLeaveRequestApprove(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 3
    leave.save()

    return redirect("faculty:supervisor_request")


@login_required
@faculty_required
def SVLeaveRequestCancel(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 12
    leave.save()
    return redirect("faculty:supervisor_request")


@login_required
@faculty_required
def TALeaveHistory(request):
    # for main function
    StudentstofFaculty = Student.objects.all().filter(TA_instructor=request.user)
    AllLeavesofStudent = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=StudentstofFaculty)).order_by('-pk')

    # for count leave request
    FacultyStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=FacultyStudent)).count()
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=StudentstofFaculty)).count()

    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=FacultyStudent)).order_by('-pk').count()
    TaHistory = AllLeavesofStudent.count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/TaHistory.html', {"AllLeaves": AllLeavesofStudent,
                                                          'TaLength': TaLength,
                                                          'SvLength': SvLength,
                                                          'TaHistory': TaHistory,
                                                          'SvHistory': SvHistory,
                                                          'user_obj': user_obj,
                                                          })
    except:
        return render(request, 'faculty/TaHistory.html', {"AllLeaves": AllLeavesofStudent,
                                                          'TaLength': TaLength,
                                                          'SvLength': SvLength,
                                                          'TaHistory': TaHistory,
                                                          'SvHistory': SvHistory,
                                                          })


@login_required
@faculty_required
def SVLeaveHistory(request):
    # main function
    StudentstofFaculty = Student.objects.all().filter(Supervisor_1=request.user)
    AllLeavesofStudent = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=StudentstofFaculty)).order_by('-pk')

    # for count leave request
    FacultyStudent = Student.objects.all().filter(TA_instructor=request.user)
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=FacultyStudent)).count()
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=StudentstofFaculty)).count()

    # for count history
    TaHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=FacultyStudent)).order_by('-pk').count()
    SvHistory = AllLeavesofStudent.count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/SvHistory.html', {"AllLeaves": AllLeavesofStudent,
                                                          'TaLength': TaLength,
                                                          'SvLength': SvLength,
                                                          'SvHistory': SvHistory,
                                                          'TaHistory': TaHistory,
                                                          'user_obj': user_obj,
                                                          })
    except:
        return render(request, 'faculty/SvHistory.html', {"AllLeaves": AllLeavesofStudent,
                                                          'TaLength': TaLength,
                                                          'SvLength': SvLength,
                                                          'SvHistory': SvHistory,
                                                          'TaHistory': TaHistory,

                                                          })


@login_required
@faculty_required
def SaveComments(request,pk):
    save = False
    leave = ApplyLeave.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.Leave = leave
            if leave.LeaveId.TA_instructor == request.user.username:
                comment.Person = "TA Instructor"
            elif leave.LeaveId.Supervisor_1 == request.user.username:
                comment.Person = "Supervisor"
            comment.save()
            save = True
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()

    StudentstofFaculty = Student.objects.all().filter(TA_instructor=request.user)
    AllLeavesofStudent = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=StudentstofFaculty)).order_by('-pk')

    # for count leave request
    FacultyStudent = Student.objects.all().filter(Q(Supervisor_1=request.user))
    SvLength = ApplyLeave.objects.all().filter(Q(Flag=2) & Q(LeaveId__in=FacultyStudent)).count()
    TaLength = ApplyLeave.objects.all().filter(Q(Flag=1) & Q(LeaveId__in=StudentstofFaculty)).count()

    # for count leave history
    SvHistory = ApplyLeave.objects.all().filter(Q(Flag=5) & Q(LeaveId__in=FacultyStudent)).order_by('-pk').count()
    TaHistory = AllLeavesofStudent.count()

    try:
        user_obj = Faculty.objects.get(user=request.user)
        return render(request, 'faculty/TA_Comment.html',{'user_obj': user_obj,
                                                          'profile_form': comment_form,
                                                          'save': save,
                                                          'leave':leave,
                                                          'TaLength': TaLength,
                                                          'SvLength': SvLength,
                                                          'SvHistory': SvHistory,
                                                          'TaHistory': TaHistory,
                                                          })
    except:
        return render(request, 'faculty/TA_Comment.html', {'profile_form': comment_form,
                                                           'save': save,
                                                           'leave':leave,
                                                           'TaLength': TaLength,
                                                           'SvLength': SvLength,
                                                           'SvHistory': SvHistory,
                                                           'TaHistory': TaHistory,
                                                           })
