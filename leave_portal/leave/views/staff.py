from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..forms import StaffSignUpForm, StaffProfileInfoForm, StaffProfileUpdateForm, CommentForm
from ..models import User, Staff, ApplyLeave, Student, Comments
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import staff_required
from django.db.models import Q


class StaffSignUpView(CreateView):
    model = User
    form_class = StaffSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'staff'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('staff:staff_profile')


@login_required
@staff_required
def staff_dash_board(request):
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()
    # count leave history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Staff.objects.get(user=request.user)
        return render(request, 'staff/staff_homepage.html', {'user_obj': user_obj,
                                                              'leavecount': leavecount,
                                                              'historycount': historycount})
    except:
        return redirect('staff:staff_profile')


@login_required
@staff_required
def staff_profile(request):
    save = False
    if request.method == "POST":

        profile_form = StaffProfileInfoForm(data=request.POST)

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

        profile_form = StaffProfileInfoForm()
    # count leave request
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()
    # count leave history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Staff.objects.get(user=request.user)
        return render(request, 'staff/staff_homepage.html',{'user_obj': user_obj,
                                                           'profile_form': profile_form,
                                                           'save': save,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount})
    except:
        return render(request, 'staff/staff_profile.html', {'profile_form': profile_form,
                                                            'save': save,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount})


@method_decorator([login_required, staff_required], name='dispatch')
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = Staff
    form_class = StaffProfileUpdateForm
    template_name = "staff/edit_profile.html"

    def get_context_data(self, **kwargs):
        user2 = get_object_or_404(User, pk=self.kwargs['pk'])
        user_obj = Staff.objects.get(user=user2)
        leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()
        historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
        kwargs['user_obj'] = user_obj
        kwargs['leavecount'] = leavecount
        kwargs['historycount'] = historycount
        return super().get_context_data(**kwargs)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.staffs

    def get_success_url(self, *args, **kwargs):
        return reverse("staff:staff_dash_board")


@login_required
@staff_required
def AllLeaveRequest(request):
    LeaveAppliedStudent = ApplyLeave.objects.all().filter(Q(Flag=3))
    # count leave request
    leavecount = LeaveAppliedStudent.count()
    # count leave history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Staff.objects.get(user=request.user)
        return render(request, 'staff/LeaveRequest.html', {
                                                            'user_obj': user_obj,
                                                            'leaverequest': LeaveAppliedStudent,
                                                            'leavecount':leavecount,
                                                            'historycount': historycount})
    except:
        return render(request, 'staff/LeaveRequest.html', {'leaverequest': LeaveAppliedStudent,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount})


@login_required
@staff_required
def AllLeaveRequestApprove(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 4
    leave.save()
    return redirect("staff:leave_request")


@login_required
@staff_required
def AllLeaveRequestCancel(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 13
    leave.save()
    return redirect("staff:leave_request")


@login_required
@staff_required
def AllLeaveHistory(request):
    AllHistory = ApplyLeave.objects.all().filter(Q(Flag=5))
    # count history
    historycount = AllHistory.count()
    # count request leave
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()

    try:
        user_obj = Staff.objects.get(user=request.user)
        return render(request, 'staff/LeaveHistory.html', {
                                                            'user_obj': user_obj,
                                                            'leavehistory': AllHistory,
                                                            'leavecount':leavecount,
                                                            'historycount':historycount})
    except:
        return render(request, 'staff/LeaveHistory.html', {'leavehistory': AllHistory,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount})

@login_required
@staff_required
def SaveComments(request,pk):
    save = False
    leave = ApplyLeave.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.Leave = leave
            comment.Person = "Office"
            comment.save()
            save = True
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()


    # count history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    # count request leave
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()
    try:
        user_obj = Staff.objects.get(user=request.user)
        return render(request, 'staff/staff_Comment.html',{'user_obj': user_obj,
                                                           'profile_form': comment_form,
                                                           'save': save,
                                                           'leave':leave,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount
                                                           })
    except:
        return render(request, 'staff/staff_Comment.html', {'profile_form': comment_form,
                                                            'save': save,
                                                            'leave':leave,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount
                                                            })


@login_required
@staff_required
def ShowMtechList(request):
    AllMtech = Student.objects.all().filter(Q(course = "Mtech"))
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()

    return render(request, 'staff/MtechList.html', {'mtechlist': AllMtech,
                                                       'leavecount': leavecount,
                                                       'historycount': historycount})

@login_required
@staff_required
def ShowPhdList(request):
    AllPhd = Student.objects.all().filter(Q(course = "Phd"))
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=3)).count()
    return render(request, 'staff/PhdList.html', {'phdlist': AllPhd,
                                                    'leavecount': leavecount,
                                                    'historycount': historycount})



@login_required
@staff_required
def ResetOdinaryLeaves(request):
    AllStud = Student.objects.all()
    for stud in AllStud:
        if stud.Odinary <= 15:
            stud.Odinary = stud.Odinary + 15
        else:
            stud.Odinary = 30
        stud.save()
    return redirect("staff:staff_dash_board")


@login_required
@staff_required
def ResetAcademicAndMedicalLeaves(request):
    AllStud = Student.objects.all()
    for stud in AllStud:

        if stud.Medical <= 15:
            stud.Medical = stud.Medical + 15
        else:
            stud.Medical = 30
        if stud.course == "Mtech":
            if stud.Acedemic <= 15:
                stud.Acedemic = stud.Acedemic + 30
            else:
                stud.Acedemic = 45
        else:
            if stud.Acedemic <= 15:
                stud.Acedemic = stud.Acedemic + 45
            else:
                stud.Acedemic = 45

        stud.save()
    return redirect("staff:staff_dash_board")