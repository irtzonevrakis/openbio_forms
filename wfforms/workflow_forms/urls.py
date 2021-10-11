from django.urls import path

from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('upload/', views.upload, name='upload'),
        path('workflows/<str:workflow_name>/', views.render_form, name='render_form'),
        path('files/<str:uid>/<str:fname>', views.get_file, name='get_file'),
]
