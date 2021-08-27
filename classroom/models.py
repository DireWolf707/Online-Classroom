from django.db import models
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.dispatch import receiver
from django.db.models.signals import pre_save

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


@receiver(pre_save, sender=Classroom)
def slugify_title(sender, instance, raw, using, update_fields, *args, **kwargs):
    instance.code = get_random_string(length=10)
