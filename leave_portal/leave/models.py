from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from _datetime import datetime
from multiselectfield import MultiSelectField
# Create your models here.
HOSTEL_CHOICES = (
    ('Barak', 'Barak'),
    ('Bramhaputra', 'Bramhaputra'),
    ('Dhansiri', 'Dhansiri'),
    ('Dibang', 'Dibang'),
    ('Dihing', 'Dihing'),
    ('Kameng', 'Kameng'),
    ('Kapili', 'Kapili'),
    ('Lohit', 'Lohit'),
    ('Manas', 'Manas'),
    ('Siang', 'Siang'),
    ('Subansiri', 'Subansiri'),
    ('Umiam', 'Umiam'),
    ('Married_Scholar', 'Married_Scholar'),
    ('NA', 'NA'),

)
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female')
)
TYPEOFLEAVE = (
    ('Odinary', 'Odinary'),
    ('Medical', 'Medical'),
    ('Acedemic', 'Acedemic'),
    ('Maternity', 'Maternity'),
    ('paternity', 'paternity')
)
COURSE = (
    ('Mtech', 'Mtech'),
    ('Phd', 'Phd'),
    ('NA', 'NA')
)

ACADEMIC_YEAR = (
    (1, ("1")),
    (2, ("2")),
    (3, ("3")),
    (4, ("4")),
    (5, ("5")),
    (6, ("6")),
    (7, ("7")),
)

SEMESTER = (
    (1, ("1")),
    (2, ("2")),
    (3, ("3")),
    (4, ("4")),
    (5, ("5")),
    (6, ("6")),
    (7, ("7")),
)
SENT_TO = (('1', 'Supervisor'),
           ('2', 'TAinstructor'),
           ('3', 'DPPC'))


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_faculty = models.BooleanField(default=False)
    is_office = models.BooleanField(default=False)
    is_dppc = models.BooleanField(default=False)
    is_hod = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='students')
    Name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='student', blank=True, null=True)
    roll_no = models.CharField(max_length=128, blank=False, default=" ", unique=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=False)
    webmail = models.CharField(max_length=128, blank=False, unique=True)
    course = models.CharField(max_length=128, choices=COURSE, blank=True)
    acedemic_year = models.IntegerField(choices=ACADEMIC_YEAR, default=0)
    present_semester = models.IntegerField(choices=SEMESTER, null=True, blank=True)
    hostel_name = models.CharField(max_length=255, choices=HOSTEL_CHOICES, blank=True, default="")
    room_number = models.CharField(max_length=10, blank=True, default="")
    mob_number = models.CharField(max_length=15, blank=False, default=" ")
    emergency_mob_num = models.CharField(max_length=15, blank=True, default=" ")
    TA_instructor = models.CharField(max_length=200, blank=True, default="", )
    Supervisor_1 = models.CharField(max_length=200, blank=True, default="")
    Odinary = models.IntegerField( blank=False, default=15)
    Medical = models.IntegerField( blank=False, default=15)
    Acedemic = models.IntegerField( blank=False, default=30)
    Maternity = models.IntegerField( blank=False, default=135)
    Paternity = models.IntegerField( blank=False, default=15)


    def __str__(self):
        return self.user.username


class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='facultys')
    Name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='faculty', blank=True, null=True, default=" ")
    faculty_id = models.CharField(max_length=128, blank=False)
    webmail = models.CharField(max_length=128, blank=False)
    mob_num = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.user.username


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staffs')
    Name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='staff', blank=True, null=True)
    staff_id = models.CharField(max_length=128, blank=False)
    webmail = models.CharField(max_length=128, blank=False)
    mob_num = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.user.username


class Hod(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='hods')
    Name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='hod', blank=True, null=True)
    hod_id = models.CharField(max_length=128, blank=False)
    webmail = models.CharField(max_length=128, blank=False)
    mob_num = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.user.username

class Dppc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dppcs')
    Name = models.CharField(max_length=200, blank=True, default="")
    profile_pic = models.ImageField(upload_to='dppc', blank=True, null=True)
    dppc_id = models.CharField(max_length=128, blank=False)
    webmail = models.CharField(max_length=128, blank=False)
    mob_num = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.user.username


class ApplyLeave(models.Model):
    LeaveId = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applyleaves')
    LeaveFrom = models.DateField()
    LeaveTo = models.DateField()
    TypeOfLeave = models.CharField(max_length=255, choices=TYPEOFLEAVE, blank=False, default="")

    ReasonForLeave = models.CharField(max_length=200)
    Doc1 = models.FileField(upload_to='documents', blank=True, null=True)
    Doc2 = models.FileField(upload_to='documents', blank=True, null=True)
    AddressWhileOnLeave = models.CharField(max_length=200)
    PhoneNumberWhileOnLeave = models.CharField(max_length=20)
    DateOfApply = models.DateField(default=datetime.now)
    Flag = models.IntegerField(default=0)
    SentTo = MultiSelectField(choices=SENT_TO)
    # Supervisor = models.IntegerField(default=0)
    # TAinstructor = models.IntegerField(default=0)
    # DPPC = models.IntegerField(default=0)

    def __str__(self):
        return self.LeaveId.Name


class Comments(models.Model):
    Leave = models.ForeignKey(ApplyLeave, on_delete=models.CASCADE, related_name='comments')
    Remark = models.CharField(max_length=200)
    Person = models.CharField(max_length=40)
    DateOfComment = models.DateField(default=datetime.now)
    def __str__(self):
        return self.Person
