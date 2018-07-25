from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_faculty:
            return redirect('faculty:fac_dash_board')
        elif request.user.is_student:
            return redirect('students:stud_dash_board')
        elif request.user.is_office:
            return redirect('staff:staff_dash_board')
        elif request.user.is_hod:
            return redirect('hod:hod_dash_board')
        elif request.user.is_dppc:
            return redirect('dppc:dppc_dash_board')
        else:
            return redirect('signup')

    return render(request, 'home.html')


# def handler404(request):
#     return render(request, '404.html', status=404)
#
# def handler500(request):
#     return render(request, '500.html', status=500)