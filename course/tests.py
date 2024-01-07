from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from course.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(email='admin@admin.admin', password='123qweasd')
        self.client = APIClient()
        token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.lesson = Lesson.objects.create(name='Тестовый урок',
                                            description='test lesson',
                                            owner=self.user)

    data = {'name': 'Тестовый урок', 'description': 'test lesson'}

    def test_create_lesson(self):
        """Тест создания урока"""

        response = self.client.post(reverse('course:lesson_create'), data=self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'course_id': None,
                                           'description': 'test lesson',
                                           'id': 2, 'name': 'Тестовый урок',
                                           'owner': None, 'preview': None, 'url': None})
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        response = self.client.get(reverse('course:lesson_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'count': 1, 'next': None,
                                           'previous': None, 'results':
                                               [{'id': 3, 'name': 'Тестовый урок',
                                                 'preview': None, 'description': 'test lesson',
                                                 'url': None, 'course_id': None, 'owner': 2}]})

    def test_retrieve_lesson(self):
        """Тест на просмотр урока"""
        response = self.client.get(reverse('course:lesson_detail', args=[self.lesson.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 4, 'name': 'Тестовый урок',
                                           'preview': None, 'description': 'test lesson',
                                           'url': None, 'course_id': None, 'owner': 3})

    def test_update_lesson(self):
        """Тест на изменение урока"""
        response = self.client.patch(reverse('course:lesson_update', args=[self.lesson.id]), data={'description': 'TEST UPDATE'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 5, 'name': 'Тестовый урок',
                                           'preview': None, 'description': 'TEST UPDATE',
                                           'url': None, 'course_id': None, 'owner': 4})

    # def test_delete_lesson(self):
    #     """Тест на удаление урока"""
    #     test_del = Lesson.objects.create(name='Тестовый урок yf elfktybt', description='test lesson del', owner=self.user)
    #     response = self.client.delete('course:lesson_delete', args=[test_del.id])
    #
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertFalse(Lesson.objects.all().exists())


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
