from course.apps import CourseConfig
from rest_framework.routers import DefaultRouter
from django.urls import path

from course.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, \
    LessonUpdateAPIView, LessonDestroyAPIView, SubscriptionCreateAPIView, SubscriptionDestroyAPIView

app_name = CourseConfig.name

router = DefaultRouter()
router.register(prefix=r'course', viewset=CourseViewSet, basename='course')
urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
    path('course/<int:pk>/create_sub/', SubscriptionCreateAPIView.as_view(), name='subscription-create'),
    path('course/<int:pk>/delete_sub/', SubscriptionDestroyAPIView.as_view(), name='subscription-delete'),

]+router.urls
