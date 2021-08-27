from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'))
    is_teacher = models.BooleanField(_('Are You a Teacher'), default=False)
