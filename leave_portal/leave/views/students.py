from django.contrib.auth import login
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from ..forms import StudentSignUpForm, StudentProfileInfoForm, StudentProfileUpdateForm, ApplyLeaveForm, CommentForm, StudentLeaveInfoForm
from ..models import Student, User, Faculty, Staff, ApplyLeave, Comments
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from ..decorators import student_required
from django.http import HttpResponse
from django.db.models import Q


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:stud_profile')


@login_required
@student_required
def stud_dash_board(request):
    try:
        user_obj = Student.objects.get(user=request.user)
        return render(request, 'student/LeaveInfo.html', {'user_obj': user_obj})
    except:
        return redirect('students:stud_profile')

@login_required
@student_required
def MyProfile(request):
    user_obj = Student.objects.get(user=request.user)
    return render(request, 'student/MyProfile.html', {'user_obj': user_obj})



@login_required
@student_required
def stud_profile(request):
    save = False
    if request.method == "POST":
        profile_form = StudentProfileInfoForm(data=request.POST)
        leave_form = StudentLeaveInfoForm(data=request.POST)
        if profile_form.is_valid():
            #print(profile_form.Name)
            profile = profile_form.save(commit=False)
            profile.user = request.user
            print(profile.Name)
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()


        else:
            print(profile_form.errors)

        if leave_form.is_valid():
            leave =  leave_form.save(commit=False)
            student = Student.objects.get(user=request.user)

            student.Odinary = leave.Odinary
            student.Medical = leave.Medical
            student.Acedemic = leave.Acedemic
            student.Maternity = leave.Maternity
            student.Paternity = leave.Paternity
            student.save()
            save = True
        else:
            print(leave_form.errors)


    else:

        profile_form = StudentProfileInfoForm()
        leave_form = StudentLeaveInfoForm()


    try:
        user_obj = Student.objects.get(user=request.user)
        return render(request, 'student/stud_dashboard.html',
                      {'user_obj': user_obj,
                       'profile_form': profile_form,
                       'save': save,
                       'leave_form':leave_form})
    except:
        return render(request, 'student/stud_profile.html', {'profile_form': profile_form,
                                                             'save': save,
                                                             'leave_form':leave_form})


@method_decorator([login_required, student_required], name='dispatch')
class EditUserProfileView(UpdateView):  # Note that we are using UpdateView and not FormView
    model = Student
    form_class = StudentProfileUpdateForm
    template_name = "student/edit_profile.html"

    def get_context_data(self, **kwargs):
        user2 = get_object_or_404(User, pk=self.kwargs['pk'])
        user_obj = Student.objects.get(user=user2)
        kwargs['user_obj'] = user_obj
        return super().get_context_data(**kwargs)

    def get_object(self, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        return user.students

    def get_success_url(self, *args, **kwargs):
        return reverse('students:stud_dash_board')


@login_required
@student_required
def ApplyLeave1(request):
    save = False
    error = False
    if request.method == "POST":

        profile_form = ApplyLeaveForm(data=request.POST)

        if profile_form.is_valid():
            profile = profile_form.save(commit=False)
            student = Student.objects.get(user=request.user)
            profile.LeaveId = student
            if 'Doc1' in request.FILES:
                profile.Doc1 = request.FILES['Doc1']
            if 'Doc2' in request.FILES:
                profile.Doc2 = request.FILES['Doc2']

            save = True

            temp = profile.SentTo
            if '1' in temp and '2' in temp and '3' not in temp:
                profile.Flag = 1
                print("1")
            elif '1' in temp and '2' not in temp and '3' not in temp:
                profile.Flag = 2
                print("2")
            elif '2' in temp and '1' not in temp and '3' not in temp:
                profile.Flag = 1
                print("3")
            elif '3' in temp and '1' not in temp and '2' not in temp:
                profile.Flag = 7
                print("4")
            else:
                error = True
                save = False
                print("5")
            profile.save()
            

        else:
            print(profile_form.errors)

    else:

        profile_form = ApplyLeaveForm()

    try:
        user_obj = Student.objects.get(user=request.user)
        return render(request, 'student/apply_leave.html',
                      {'user_obj': user_obj, 'profile_form': profile_form, 'save': save,'error':error})
    except:
        return render(request, 'student/apply_leave.html', {'profile_form': profile_form,
                                                            'save': save,'error':error})


@login_required
@student_required
def CurrentStatus(request):
    CurrentStudent = Student.objects.get(user=request.user)
    CurrentRequest = ApplyLeave.objects.all().filter(LeaveId=CurrentStudent).order_by('-pk')
    if len(CurrentRequest) > 0:
        CurrentLeave = CurrentRequest[0]
    else:
        CurrentLeave = []

    try:
        user_obj = Student.objects.get(user=request.user)
        return render(request, 'student/currentleave.html', {'currleave': CurrentLeave,
                                                             'user_obj': user_obj})
    except:
        return render(request, 'student/currentleave.html', {'currleave': CurrentLeave})



@login_required
@student_required
def History(request):
    CurrentStudent = Student.objects.get(user=request.user)
    Currentrequest = ApplyLeave.objects.all().filter(LeaveId=CurrentStudent).order_by('-pk')[1:]
    try:
        user_obj = Student.objects.get(user=request.user)
        return render(request, 'student/history.html', {'currleave': Currentrequest,
                                                        'user_obj': user_obj})

    except:
        return render(request, 'student/history.html', {'currleave': Currentrequest})

@login_required
@student_required
def ShowComments(request):
    CurrentStudent = Student.objects.get(user=request.user)
    CurrentRequest = ApplyLeave.objects.all().filter(LeaveId=CurrentStudent).order_by('-pk')
    if len(CurrentRequest):
       CurrentLeave = CurrentRequest[0]
       Comment = Comments.objects.all().filter(Leave=CurrentLeave).order_by('-pk')
    else:
        Comment = False
    return render(request, 'student/ShowComments.html', {'comments': Comment})


@login_required
@student_required
def PastComments(request,pk):

    Currentleave = ApplyLeave.objects.get(pk=pk)
    Comment = Comments.objects.all().filter(Leave=Currentleave)
    if not len(Comment):
        Comment = False
    return render(request, 'student/ShowComments.html', {'comments': Comment})