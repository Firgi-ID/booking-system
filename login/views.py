from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# @login_required
# def dashboard_view(request):
#     return render(request, 'dashboard.html')

def group_check(request):
    group_name = Group.objects.filter(user=request.user)  # get logged-in user's group
    if not group_name:
        raise Http404("Group not found for user.")

    group_name = str(group_name[0])  # convert to string

    if group_name == "Student":
        return redirect('http://127.0.0.1:8000/student/')
    elif group_name == "Teacher":
        return redirect('http://127.0.0.1:8000/teacher/')
    else:
        raise Http404("User group not recognized.")

def logout_view(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

class register_teacher(TemplateView):
    template_name = "register_teacher.html"

class register_student(TemplateView):
    template_name = "register_student.html"
