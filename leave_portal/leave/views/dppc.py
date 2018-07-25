from django.contrib.auth import login
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, TemplateView)

from ..forms import DppcSignUpForm, DppcProfileInfoForm, DppcProfileUpdateForm, CommentForm
from ..models import User, Dppc, ApplyLeave
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import dppc_required
from django.db.models import Q


class DppcSignUpView(CreateView):
    model = User
    form_class = DppcSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'DPPC'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('dppc:dppc_profile')


@login_required
@dppc_required
def dppc_dash_board(request):
    # for count leave request
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=7)).count()
    # for leave history
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Dppc.objects.get(user=request.user)
        return render(request, 'dppc/dppc_dashboard.html', {'user_obj': user_obj,
                                                          'leavecount': leavecount,
                                                          'historycount': historycount})
    except:
        return redirect('dppc:dppc_profile')


@login_required
@dppc_required
def dppc_profile(request):
    save = False
    if request.method == "POST":

        profile_form = DppcProfileInfoForm(data=request.POST)

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

        profile_form = DppcProfileInfoForm()

    leavecount = ApplyLeave.objects.all().filter(Q(Flag=7)).count()
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Dppc.objects.get(user=request.user)
        return render(request, 'dppc/dppc_dashboard.html',{'user_obj': user_obj,
                                                       'profile_form': profile_form,
                                                       'save': save,
                                                       'leavecount': leavecount,
                                                       'historycount': historycount})
    except:
        return render(request, 'dppc/dppc_profile.html', {'profile_form': profile_form,
                                                        'save': save,
                                                        'leavecount': leavecount,
                                                        'historycount': historycount})


@method_decorator([login_required, dppc_required], name='dispatch')
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = Dppc
    form_class = DppcProfileUpdateForm
    template_name = "dppc/edit_profile.html"

    def get_context_data(self, **kwargs):
        user2 = get_object_or_404(User, pk=self.kwargs['pk'])
        user_obj = Dppc.objects.get(user=user2)
        leavecount = ApplyLeave.objects.all().filter(Q(Flag=7)).count()
        historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
        kwargs['user_obj'] = user_obj
        kwargs['leavecount'] = leavecount
        kwargs['historycount'] = historycount
        return super().get_context_data(**kwargs)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.dppcs

    def get_success_url(self, *args, **kwargs):
        return reverse("dppc:dppc_dash_board")


@login_required
@dppc_required
def AllLeaveRequest(request):
    LeaveAppliedStudent = ApplyLeave.objects.all().filter(Q(Flag=7))
    leavecount = LeaveAppliedStudent.count()
    historycount = ApplyLeave.objects.all().filter(Q(Flag=5)).count()
    try:
        user_obj = Dppc.objects.get(user=request.user)
        return render(request, 'dppc/DppcLeaveRequest.html', {
                                                            'user_obj': user_obj,
                                                            'leaverequest': LeaveAppliedStudent,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount})
    except:
        return render(request, 'dppc/DppcLeaveRequest.html', {'leaverequest': LeaveAppliedStudent,
                                                            'leavecount': leavecount,
                                                            'historycount': historycount})


@login_required
@dppc_required
def AllLeaveRequestApprove(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 3
    leave.save()
    return redirect("dppc:leave_request")


@login_required
@dppc_required
def AllLeaveRequestCancel(request, pk):
    leave = ApplyLeave.objects.get(pk=pk)
    leave.Flag = 17
    leave.save()
    return redirect("dppc:leave_request")


@login_required
@dppc_required
def AllLeaveHistory(request):
    AllHistory = ApplyLeave.objects.all().filter(Q(Flag=5))
    # count history
    historycount = AllHistory.count()
    # count request leave
    leavecount = ApplyLeave.objects.all().filter(Q(Flag=7)).count()

    try:
        user_obj = Dppc.objects.get(user=request.user)
        return render(request, 'dppc/dppcleavehistory.html', {
                                                            'user_obj': user_obj,
                                                            'leavehistory': AllHistory,
                                                            'leavecount':leavecount,
                                                            'historycount':historycount})
    except:
        return render(request, 'dppc/dppcleavehistory.html', {'leavehistory': AllHistory,
                                                           'leavecount': leavecount,
                                                           'historycount': historycount})

@login_required
@dppc_required
def SaveComments(request,pk):
    save = False
    leave = ApplyLeave.objects.get(pk=pk)
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.Leave = leave
            comment.Person = "Dppc"
            comment.save()
            save = True
        else:
            print(comment_form.errors)
    else:
        comment_form = CommentForm()
    try:
        user_obj = Dppc.objects.get(user=request.user)
        return render(request, 'dppc/dppc_Comment.html',{'user_obj': user_obj,
                                                       'profile_form': comment_form,
                                                       'save': save,
                                                       'leave':leave})
    except:
        return render(request, 'dppc/dppc_Comment.html', {'profile_form': comment_form,
                                                        'save': save,
                                                        'leave':leave})