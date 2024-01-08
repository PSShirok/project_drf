from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from course.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    data = {'name': 'Тестовый урок', 'description': 'test lesson'}

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='admin@admin.admin', password='123qweasd')
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.lesson = Lesson.objects.create(name='Тестовый урок',
                                            description='test lesson',
                                            owner=self.user)

    def test_create_lesson(self):
        """Тест создания урока"""

        response = self.client.post(reverse('course:lesson_create'), data=self.data)
        lesson = Lesson.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'course_id': None,
                                           'description': lesson.description,
                                           'id': lesson.id, 'name': lesson.name,
                                           'owner': None, 'preview': None, 'url': None})
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('course:lesson_list'))
        lesson = Lesson.objects.last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 1, 'next': None,
                                           'previous': None, 'results':
                                               [{'id': lesson.id, 'name': lesson.name,
                                                 'preview': None, 'description': lesson.description,
                                                 'url': None, 'course_id': None, 'owner': lesson.owner.id}]})

    def test_retrieve_lesson(self):
        """Тест на просмотр урока"""
        response = self.client.get(reverse('course:lesson_detail', args=[self.lesson.id]))
        lesson = Lesson.objects.last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': lesson.id, 'name': lesson.name,
                                           'preview': None, 'description': lesson.description,
                                           'url': None, 'course_id': None, 'owner': lesson.owner.id})

    def test_update_lesson(self):
        """Тест на изменение урока"""
        response = self.client.patch(reverse('course:lesson_update', args=[self.lesson.id]),
                                     data={'description': 'TEST UPDATE'})
        lesson = Lesson.objects.last()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': lesson.id, 'name': lesson.name,
                                           'preview': None, 'description': lesson.description,
                                           'url': None, 'course_id': None, 'owner': lesson.owner.id})

    def test_delete_lesson(self):
        """Тест на удаление урока"""
        lesson = Lesson.objects.last()
        response = self.client.delete(reverse('course:lesson_delete', args=[lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.all().exists())


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='admin@admin.admin', password='123qweasd')
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.course = Course.objects.create(
            name='test_course',
            description='test_course',
            owner=self.user
        )

    def test_create(self):
        """Тестирование создания подписки"""
        subscription = {"user": self.user.pk, "course": self.course.pk}

        response = self.client.post(reverse('course:subscription-create',
                                            kwargs={'pk': self.course.pk}),
                                    data=subscription)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete(self):
        """Тестирование удаления подписки"""

        course = Subscription.objects.create(user=self.user, course=self.course)

        response = self.client.delete(reverse('course:subscription-delete',
                                              kwargs={'pk': course.pk}))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
