from lesson.apps import LessonConfig
from rest_framework import generics
from django.urls import path

from lesson.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = LessonConfig.name


urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('', LessonListAPIView.as_view(), name='lesson_list'),
    path('<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),


]
