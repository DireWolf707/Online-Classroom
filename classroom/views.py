from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from .models import Classroom
from .forms import CreateClassForm, JoinClassForm


class HomeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_teacher:
            classrooms = user.classrooms.all()
            form = CreateClassForm()
        else:
            classrooms = Classroom.objects.filter(
                students__in=[self.request.user]
            )
            form = JoinClassForm()
        return render(request, 'home.html', {'classrooms': classrooms, 'form': form})


class CreateClassView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        form = CreateClassForm(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        form.save()
        messages.info(self.request, 'Classroom Created!')
        return redirect('home')

    def form_invalid(self, form):
        messages.warning(
            self.request, 'Some Error Occured: Classroom Not Created!')
        return redirect('home')

    def test_func(self):
        return self.request.user.is_teacher


class JoinClassView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        form = JoinClassForm(data=self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        classroom = Classroom.objects.filter(code=form.cleaned_data['code'])
        if classroom.exists():
            classroom.first().students.add(self.request.user)
            messages.info(self.request, 'Classroom Joined!')
            return redirect('home')
        messages.info(self.request, 'Classroom Not Found!')
        return redirect('home')

    def form_invalid(self, form):
        messages.warning(
            self.request, 'Some Error Occured: Classroom Not Joined!')
        return redirect('home')

    def test_func(self):
        return not self.request.user.is_teacher
