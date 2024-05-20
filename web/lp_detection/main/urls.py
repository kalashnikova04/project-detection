from django.urls import path

from . import views

app_name = "main"
urlpatterns = [
    path("", views.index, name="index"),
    path("train/", views.train_yolo, name="train"),
    path("model_mode/", views.send_inference_task, name="mode"),
    path("task_status/", views.update_task_status, name="update_status"),
    path("inference/", views.get_prediction, name="detection_results"),
]
