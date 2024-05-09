from django.urls import path

from . import views

app_name = 'main'
urlpatterns = [
    path('', views.index, name='index'),
    path('train/', views.train_yolo, name='train'),
    path('pred/', views.get_prediction, name='detection'),
    # path('upoad/', views.site.urls),
]



