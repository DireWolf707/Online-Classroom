from django.urls import path
from .views import HomeView, CreateClassView, JoinClassView

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("create_class/", CreateClassView.as_view(), name='create_class'),
    path("join_class/", JoinClassView.as_view(), name='join_class'),
]
