from django.urls import path
from . import views
from django.contrib.auth.views import LoginView


# urlpatterns = [
#     path('dashboard/', views.dashboard_view, name='dashboard'),
# ]

from .views import (
    group_check,
    logout_view,
    register_teacher,
    register_student,
)

urlpatterns = [
    path('', LoginView.as_view(template_name='index.html'), name="home"),
    path('logout/', logout_view, name='logout'),
    path('group/', group_check, name='group'),
    path('register_teacher/', register_teacher.as_view(), name='register_teacher'),
    path('register_student/', register_student.as_view(), name='register_student'),

]
