from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Classroom


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_teacher:
            classrooms = user.classrooms.all()
        else:
            classrooms = Classroom.objects.filter(
                students__in=[self.request.user]
            )
        return render(request, 'home.html', {'classrooms': classrooms})
