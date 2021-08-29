from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.template.loader import render_to_string

User = get_user_model()


class Classroom(models.Model):
    teacher = models.ForeignKey(
        User, related_name='classrooms', on_delete=models.CASCADE
    )
    name = models.CharField(max_length=30, blank=True)
    code = models.CharField(max_length=10, blank=True)
    students = models.ManyToManyField(
        User, related_name='student_joined', blank=True
    )

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse("dashboard", kwargs={"code": self.code})


@receiver(pre_save, sender=Classroom)
def slugify_title(sender, instance, raw, using, update_fields, *args, **kwargs):
    instance.code = get_random_string(length=10)


class Stream(models.Model):
    classroom = models.ForeignKey(
        Classroom, on_delete=models.CASCADE, related_name='streams'
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'announcement', 'test', 'assignment',)
                                     }
                                     )
    object_id = models.PositiveIntegerField()
    stream_obj = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-id',)


class BaseStreamObject(models.Model):
    classroom = models.ForeignKey(
        Classroom, related_name='classroom_%(class)s', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=30)
    teacher = models.ForeignKey(
        User, related_name='teacher_%(class)s', on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def render(self):
        type = self._meta.model_name
        return render_to_string(f'partials/{type}.html', {'stream_obj': self, 'type': type})


class Announcement(BaseStreamObject):
    text = models.TextField()


class Test(BaseStreamObject):
    text = models.TextField(blank=True)
    max_marks = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    attachment = models.FileField(blank=True)


class Assignment(BaseStreamObject):
    text = models.TextField(blank=True)
    due_date = models.DateTimeField()
    attachment = models.FileField(blank=True)


class BaseSubmission(models.Model):
    class Status(models.TextChoices):
        LATE = 'L', 'Late'
        DONE = 'D', 'Done'

    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='student_%(class)s'
    )
    submit_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=Status.choices)
    attachment = models.FileField(blank=True)
    text = models.TextField(blank=True)

    class Meta:
        abstract = True


class AssignmentSubmission(BaseSubmission):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name='assignment_submissions'
    )
    reviewed = models.BooleanField(default=False)


class TestSubmission(BaseSubmission):
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='test_submissions'
    )
    grade = models.PositiveIntegerField(blank=True, null=True)
