from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from .models import Appointment
from .forms import AppointmentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Fungsi untuk memeriksa apakah user termasuk dalam grup tertentu
def is_in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@login_required
def teacher(request):
    if is_in_group(request.user, "Teacher"):
        user_name = request.user.get_username()
        appointment_list = Appointment.objects.filter(user=request.user).order_by("-id")

        q = request.GET.get("q")
        if q:
            appointment_list = appointment_list.filter(appointment_with__icontains=q)

        context = {
            "query": appointment_list,
            "user_name": user_name
        }
        return render(request, 'teacher.html', context)

    return redirect('home')


@login_required
def teacher_appointment_list(request):
    if is_in_group(request.user, "Teacher"):
        user_name = request.user.get_username()
        appointment_list = Appointment.objects.filter(user=request.user).order_by("-id")

        q = request.GET.get("q")
        if q:
            appointment_list = appointment_list.filter(date__icontains=q)

        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            messages.success(request, 'Appointment created successfully')
            return redirect('teacher_appointment_list')  # name sesuai urls.py

        context = {
            "query": appointment_list,
            "user_name": user_name,
            "form": form,
        }
        return render(request, 'teacher_create_appointment.html', context)

    return redirect('home')


@login_required
def appointment_delete(request, id):
    if is_in_group(request.user, "Teacher"):
        try:
            appointment = Appointment.objects.get(id=id, user=request.user)
            appointment.delete()
            messages.success(request, 'Appointment deleted successfully')
        except Appointment.DoesNotExist:
            messages.error(request, 'Appointment not found or access denied')
        return redirect('teacher_appointment_list')

    return redirect('home')


@login_required
def teacher_appointment_update(request, id):
    if is_in_group(request.user, "Teacher"):
        user_name = request.user.get_username()
        appointment_list = Appointment.objects.filter(user=request.user).order_by("-id")

        try:
            single_appointment = Appointment.objects.get(id=id, user=request.user)
        except Appointment.DoesNotExist:
            messages.error(request, "Appointment not found or access denied")
            return redirect('teacher_appointment_list')

        form = AppointmentForm(request.POST or None, instance=single_appointment)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            messages.success(request, 'Appointment updated successfully')
            return redirect('teacher_appointment_list')

        context = {
            "query": appointment_list,
            "user_name": user_name,
            "form": form,
        }
        return render(request, 'teacher_appointment_update.html', context)

    return redirect('home')
