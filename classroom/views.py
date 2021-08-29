from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.apps import apps
from django.http import Http404
from django.forms import modelform_factory
from .models import Classroom, Stream
from .forms import CreateClassForm, JoinClassForm
from django import forms
from django.utils import timezone


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


class DashboardView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        classroom = get_object_or_404(Classroom, code=self.kwargs['code'])
        streams = classroom.streams.all()
        if self.request.user.is_teacher:
            upcoming_tests = classroom.classroom_test.filter(
                due_date__gt=timezone.now()
            )
            upcoming_assignments = classroom.classroom_assignment.filter(
                due_date__gt=timezone.now()
            )
        else:
            upcoming_tests = classroom.classroom_test.filter(
                due_date__gt=timezone.now(),
            ).exclude(test_submissions__student__in=[self.request.user])
            upcoming_assignments = classroom.classroom_assignment.filter(
                due_date__gt=timezone.now()
            ).exclude(assignment_submissions__student__in=[self.request.user])
        return render(request, "dashboard.html", {'classroom': classroom, 'streams': streams, 'upcoming_tests': upcoming_tests, 'upcoming_assignments': upcoming_assignments})

# for teacher to create and update stream


class StreamCreateUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        self.set_objects()
        form = self.get_form(instance=self.stream_obj)
        return render(request, 'partials/stream_form.html', {'form': form, 'model_name': self.model_name, 'code': self.kwargs['code'], 'stream_id': self.stream_id, 'stream_obj': self.stream_obj})

    def post(self, request, *args, **kwargs):
        self.set_objects()
        form = self.get_form(
            instance=self.stream_obj, data=self.request.POST, files=self.request.FILES
        )
        if form.is_valid():
            form.instance.classroom = get_object_or_404(
                Classroom, code=self.kwargs['code'], teacher=self.request.user
            )
            form.instance.teacher = self.request.user
            stream_obj = form.save()
            # if new object is created
            if self.stream_obj is None:
                Stream.objects.create(
                    classroom=stream_obj.classroom,
                    stream_obj=stream_obj
                )
            messages.success(self.request, 'Stream Updated !')
            return redirect('dashboard', self.kwargs['code'])

        messages.warning(self.request, 'Some Error Occured !')
        return redirect('dashboard', self.kwargs['code'])

    def get_model(self, model_name):
        if model_name in ('announcement', 'test', 'assignment',):
            return apps.get_model(app_label='classroom', model_name=model_name)
        raise Http404()

    def get_form(self, *args, **kwargs):
        form = modelform_factory(self.model,
                                 exclude=('classroom', 'teacher'),
                                 widgets={
                                     'due_date': forms.DateInput(attrs={'type': 'date'})
                                 }
                                 )
        return form(*args, **kwargs)

    def set_objects(self):
        self.model_name = self.kwargs['model_name']
        self.model = self.get_model(self.model_name)
        self.stream_obj = None
        self.stream_id = self.kwargs.get('stream_id')
        if self.stream_id:
            self.stream_obj = get_object_or_404(
                self.model, id=self.stream_id, teacher=self.request.user
            )

    def test_func(self):
        return self.request.user.is_teacher

# for teacher to delete stream


class StreamDeleteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        stream = get_object_or_404(Stream, id=self.kwargs['stream_id'])
        stream_obj = stream.stream_obj
        if stream_obj.teacher != self.request.user:
            raise Http404()
        classroom = stream_obj.classroom
        stream_obj.delete()
        stream.delete()
        messages.success(self.request, 'Stream Updated !')
        return redirect('dashboard', classroom.code)

# detail view for stream (student)


class StreamDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        model_name = self.kwargs['model_name']
        model_id = self.kwargs['model_id']
        submission_id = None
        if model_name == 'assignment':
            model = apps.get_model(
                app_label='classroom', model_name='assignment'
            )
            submission_model = get_object_or_404(
                model, id=model_id
            )
            submission = submission_model.assignment_submissions.filter(
                student__in=[self.request.user]
            )
        elif model_name == 'test':
            model = apps.get_model(
                app_label='classroom', model_name='test'
            )
            submission_model = get_object_or_404(
                model, id=model_id
            )
            submission = submission_model.test_submissions.filter(
                student__in=[self.request.user]
            )
        else:
            raise Http404()
        form = modelform_factory(model, fields=('text', 'attachment',))
        if submission.exists():
            submission_id = submission[0].id
            form = form(instance=submission[0])
        else:
            form = form()
        return render(request, "partials/submission_form.html", {'form': form, 'submission_model': submission_model, "submission_id": submission_id, 'model_name': model_name, 'model_id': model_id})

    def test_func(self):
        return not self.request.user.is_teacher

# submission view for students


class SubmissionCreateUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, request, *args, **kwargs):
        self.set_objects()
        form = self.get_form(instance=self.submission)
        return render(request, "partials/submission_form.html", {'form': form, 'submission_model': self.submission_model, 'submission_id': self.submission_id, 'model_name': self.model_name, 'model_id': self.model_id})

    def post(self, request, *args, **kwargs):
        self.set_objects()
        form = self.get_form(
            instance=self.submission, data=self.request.POST, files=self.request.FILES
        )
        if form.is_valid():
            form.instance.student = self.request.user
            if self.submission_model.due_date > timezone.now():
                form.instance.status = 'D'
            else:
                form.instance.status = 'L'
            submission = form.save(commit=False)
            # if new object is created
            if self.submission is None:
                if self.model_name == 'test':
                    submission.test = self.submission_model
                else:
                    submission.assignment = self.submission_model
            submission = form.save()
            messages.success(
                self.request, f'{self.submission_model.title} ({self.model_name}) Submited !'
            )
            return redirect('dashboard', self.submission_model.classroom.code)

        messages.warning(self.request, 'Some Error Occured !')
        return redirect('dashboard', self.submission_model.classroom.code)

    def get_model(self, model_name):
        if model_name in ('assignment', 'test',):
            return apps.get_model(app_label='classroom', model_name=f'{model_name}submission')
        return Http404()

    def get_form(self, *args, **kwargs):
        form = modelform_factory(self.model, fields=('text', 'attachment',))
        return form(*args, **kwargs)

    def get_submission_model(self, model_id, model_name):
        if model_name in ('assignment', 'test',):
            model = apps.get_model(
                app_label='classroom', model_name=model_name
            )
            return get_object_or_404(model, id=model_id)
        return Http404()

    def set_objects(self):
        self.model_name = self.kwargs['model_name']
        # model(table) of test or assignment submissions
        self.model = self.get_model(self.model_name)
        # model_id for associating submission with respective assignment/test
        self.model_id = self.kwargs['model_id']
        self.submission_model = self.get_submission_model(
            self.model_id, self.model_name
        )
        # submission of test or assignment
        self.submission = None
        self.submission_id = self.kwargs.get('submission_id')
        if self.submission_id:
            self.submission = get_object_or_404(
                self.model, id=self.submission_id
            )

    def test_func(self):
        return not self.request.user.is_teacher
