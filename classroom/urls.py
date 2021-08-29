from django.urls import path
from .views import HomeView, CreateClassView, JoinClassView, DashboardView, StreamCreateUpdateView, StreamDeleteView, SubmissionCreateUpdateView, StreamDetailView

urlpatterns = [
    path("", HomeView.as_view(), name='home'),
    path("create_class/", CreateClassView.as_view(), name='create_class'),
    path("join_class/", JoinClassView.as_view(), name='join_class'),
    path("<str:code>/dashboard/", DashboardView.as_view(), name='dashboard'),
    # stream create,update,delete
    path("stream/<int:stream_id>/",
         StreamDeleteView.as_view(), name='stream_delete'),  # this id corresponds to generic object id not object id like other
    path("stream/<str:code>/<str:model_name>/",
         StreamCreateUpdateView.as_view(), name='stream_create'),
    path("stream/<str:code>/<str:model_name>/<int:stream_id>/",
         StreamCreateUpdateView.as_view(), name='stream_update'),
    path("stream_detail/<str:model_name>/<int:model_id>/",
         StreamDetailView.as_view(), name='stream_detail'),
    # submission create,update,delete
    path("submission/<str:model_name>/<int:model_id>/",
         SubmissionCreateUpdateView.as_view(), name='submission_create'),
    path("submission/<str:model_name>/<int:model_id>/<int:submission_id>/",
         SubmissionCreateUpdateView.as_view(), name='submission_update'),
]
