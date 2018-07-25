
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
#from django.forms.utils import ValidationError
from leave.models import (Student, User, Faculty, Staff, Hod, ApplyLeave, Dppc, Comments)
import datetime


class StudentSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        return user


class FacultySignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_faculty = True
        if commit:
            user.save()
        return user



class StaffSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_office = True
        if commit:
            user.save()
        return user


class HodSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_hod = True
        if commit:
            user.save()
        return user

class DppcSignUpForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_dppc = True
        if commit:
            user.save()
        return user


class StudentProfileInfoForm(forms.ModelForm):
    TA_instructor = forms.ModelChoiceField(queryset=User.objects.all().filter(is_faculty=True),required=False)
    Supervisor_1 =  forms.ModelChoiceField(queryset=User.objects.all().filter(is_faculty=True),required=False)


    class Meta():
        model = Student
        fields = ('Name','profile_pic','roll_no','webmail','gender','course',
                  'acedemic_year','present_semester','hostel_name','room_number',
                  'mob_number','emergency_mob_num','TA_instructor','Supervisor_1')

class StudentLeaveInfoForm(forms.ModelForm):

    class Meta():
        model = Student
        fields = ('Odinary','Medical','Acedemic','Maternity','Paternity')

class FacultyProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Faculty
        fields = ('Name','profile_pic','faculty_id','webmail','mob_num')


class StaffProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Staff
        fields = ('Name','profile_pic','staff_id','webmail','mob_num')


class HodProfileInfoForm(forms.ModelForm):
    class Meta():
        model = Hod
        fields = ('Name','profile_pic','hod_id','webmail','mob_num')


class DppcProfileInfoForm(forms.ModelForm):

    class Meta():
        model = Dppc
        fields = ('Name','profile_pic','dppc_id','webmail','mob_num')


class StudentProfileUpdateForm(forms.ModelForm):
    TA_instructor = forms.ModelChoiceField(queryset=User.objects.all().filter(is_faculty=True),required=False)
    Supervisor_1 = forms.ModelChoiceField(queryset=User.objects.all().filter(is_faculty=True),required=False)

    class Meta:
        model = Student
        fields = ('Name','profile_pic','roll_no','webmail','gender','course','acedemic_year',
                  'present_semester','hostel_name','room_number','mob_number','emergency_mob_num',
                  'TA_instructor','Supervisor_1') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(StudentProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class FacultyProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = ('Name','profile_pic','faculty_id','webmail','mob_num') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(FacultyProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class StaffProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('Name','profile_pic','staff_id','webmail','mob_num') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(StaffProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class HodProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Hod
        fields = ('Name','profile_pic','hod_id','webmail','mob_num') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(HodProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

class DppcProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Dppc
        fields = ('Name','profile_pic','dppc_id','webmail','mob_num') #Note that we didn't mention user field here.

    def save(self, user=None):
        user_profile = super(DppcProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile

class ApplyLeaveForm(forms.ModelForm):
    ReasonForLeave = forms.CharField(widget=forms.Textarea(attrs={'cols' : "15", 'rows': "3"}))
    LeaveFrom = forms.DateField(initial=datetime.date.today)
    LeaveTo = forms.DateField(initial=datetime.date.today)


    class Meta():
        model = ApplyLeave
        fields = ('LeaveFrom','LeaveTo','TypeOfLeave','ReasonForLeave','Doc1','Doc2','AddressWhileOnLeave','PhoneNumberWhileOnLeave','SentTo')

class CommentForm(forms.ModelForm):

    class Meta():
        model = Comments
        fields = ('Remark',)