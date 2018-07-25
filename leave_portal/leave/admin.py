from django.contrib import admin
from .models import User,Student,Faculty,Staff,Hod,ApplyLeave

# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Staff)
admin.site.register(Hod)
admin.site.register(ApplyLeave)

