from django.conf import settings
from django.core.mail import send_mail
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from course.models import Course, Lesson, Subscription
from course.paginators import CoursePaginator
from course.permissions import IsModerator, IsOwner
from course.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            permission_classes = [IsOwner]
        elif self.action == 'list' or self.action == 'retrieve' or self.action == 'update':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()

    def perform_update(self, serializer):
        serializer.save()
        pk = self.kwargs.get('pk')
        course = Course.objects.get(pk=pk)
        subscriptions = Subscription.objects.filter(course=course, is_active=True)
        emails = list(subscriptions.values_list('user__email', flat=True))
        send_mail('Course update',
                  'Course update',
                  settings.EMAIL_HOST_USER,
                  recipient_list=emails,
                  fail_silently=False)


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsOwner]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]
    pagination_class = CoursePaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    def perform_create(self, serializer, *args, **kwargs):
        subscription = serializer.save()
        subscription.user = self.request.user
        course_pk = self.kwargs.get('pk')
        subscription.course = Course.objects.get(pk=course_pk)
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]
    