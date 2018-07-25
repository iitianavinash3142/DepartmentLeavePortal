from django.conf import settings
from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..forms import HodSignUpForm, HodProfileInfoForm, HodProfileUpdateForm, CommentForm
from ..models import User, Hod, ApplyLeave, Comments, Student
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import hod_required
from django.db.models import Q
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse


class HodSignUpView(CreateView):
    model = User
    form_class = HodSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'hod'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('hod:hod_profile')


@login_required
@hod_required
def hod_dash_board(request):
    # for count leave request
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=4)).count()
    # for leave history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Hod.objects.get(user=request.user)
        return render(request, 'hod/hod_dashboard.html', {'user_obj': user_obj,
                                                          'leavecount': leavecount,
                                                          'historycount': historycount})
    except:
        return redirect('hod:hod_profile')



@login_required
@hod_required
def hod_profile(request):
    save = False
    if request.method == "POST":

        profile_form = HodProfileInfoForm(data=request.POST)

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

        profile_form = HodProfileInfoForm()

    leavecount = ApplyLeave.objects.all().filter(Q(Flag=4)).count()
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Hod.objects.get(user=request.user)
        return render(request, 'hod/hod_dashboard.html',{'user_obj': user_obj,
                                                       'profile_form': profile_form,
                                                       'save': save,
                                                       'leavecount': leavecount,
                                                       'historycount': historycount})
    except:
        return render(request, 'hod/hod_profile.html', {'profile_form': profile_form,
                                                        'save': save,
                                                        'leavecount': leavecount,
                                                        'historycount': historycount})


@method_decorator([login_required, hod_required], name='dispatch')
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = Hod
    form_class = HodProfileUpdateForm
    template_name = "hod/edit_profile.html"

    def get_context_data(self, **kwargs):
        user2 = get_object_or_404(User, pk=self.kwargs['pk'])
        user_obj = Hod.objects.get(user=user2)
        leavecount = ApplyLeave.objects.all().filter(Q(Flag=4)).count()
        historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
        kwargs['user_obj'] = user_obj
        kwargs['leavecount'] = leavecount
        kwargs['historycount'] = historycount
        return super().get_context_data(**kwargs)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.hods

    def get_success_url(self, *args, **kwargs):
        return reverse("hod:hod_dash_board")


@login_required
@hod_required
def AllLeaveRequest(request):
    LeaveAppliedStudent = ApplyLeave.objects.all().filter(Q(Flag=4))
    leavecount = LeaveAppliedStudent.count()
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Hod.objects.get(user=request.user)
        return render(request, 'hod/HodLeaveRequest.html', {
                                                            'user_obj': user_obj,
                                                            'leaverequest': LeaveAppliedStudent,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount})
    except:
        return render(request, 'hod/HodLeaveRequest.html', {'leaverequest': LeaveAppliedStudent,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount})


@login_required
@hod_required
def AllLeaveRequestApprove(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)

    leave.Flag = 5
    NoOfDays = leave.LeaveTo - leave.LeaveFrom


    if leave.TypeOfLeave == "Odinary":
        leave.LeaveId.Odinary =leave.LeaveId.Odinary - NoOfDays.days
        leave.LeaveId.save()

    if leave.TypeOfLeave == "Medical":
        leave.LeaveId.Medical =leave.LeaveId.Medical - NoOfDays.days
        leave.LeaveId.save()

    if leave.TypeOfLeave == "Acedemic":
        leave.LeaveId.Acedemic =leave.LeaveId.Acedemic - NoOfDays.days
        leave.LeaveId.save()

    if leave.TypeOfLeave == "Maternity":
        leave.LeaveId.Maternity =leave.LeaveId.Maternity - NoOfDays.days
        leave.LeaveId.save()

    if leave.TypeOfLeave == "Paternity":
        leave.LeaveId.Paternity =leave.LeaveId.Paternity - NoOfDays.days
        leave.LeaveId.save()

    # from_email = 'avinashucheniya@gmail.com'
    # subject = 'Approve'
    # message = 'Leace has approved'
    # to_list = ['sherukhan007@iitg.ac.in']
    #
    # try:
    #     send_mail(subject,message,from_email,to_list,fail_silently=False)
    # except BadHeaderError:
    #     HttpResponse('Bad Header')

    leave.save()

    return redirect("hod:leave_request")


@login_required
@hod_required
def AllLeaveRequestCancel(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 14
    leave.save()
    return redirect("hod:leave_request")


@login_required
@hod_required
def AllLeaveHistory(request):
    AllHistory = ApplyLeave.objects.all().filter(Q(Flag=5))
    # count history
    historycount = AllHistory.count()
    # count request leave
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=4)).count()

    try:
        user_obj = Hod.objects.get(user=request.user)
        return render(request, 'hod/hodleavehistory.html', {
                                                            'user_obj': user_obj,
                                                            'leavehistory': AllHistory,
                                                            'leavecount':leavecount,
                                                            'historycount':historycount})
    except:
        return render(request, 'hod/hodleavehistory.html', {'leavehistory': AllHistory,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount})


@login_required
@hod_required
def SaveComments(request,pk):
    save = False
    leave = ApplyLeave.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.Leave = leave
            comment.Person = "Hod"
            comment.save()
            save = True
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
    try:
        user_obj = Hod.objects.get(user=request.user)
        return render(request, 'hod/hod_Comment.html',{'user_obj': user_obj,
                                                       'profile_form': comment_form,
                                                       'save': save,
                                                       'leave':leave})
    except:
        return render(request, 'hod/hod_Comment.html', {'profile_form': comment_form,
                                                        'save': save,
                                                        'leave':leave})