from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.urls import reverse
from rest_framework_simplejwt.tokens import AccessToken

from course.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        pass

    data = {'name': 'Тестовый урок', 'description': 'test lesson'}

    def test_create_lesson(self):
        """Тест создания урока"""

        response = self.client.post('/lesson/create/', data=self.data)
        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {'course_id': None,
                                           'description': 'test lesson',
                                           'id': 1, 'name': 'Тестовый урок',
                                           'owner': None, 'preview': None, 'url': None})
        self.assertTrue(Lesson.objects.all().exists())

    def test_list_lesson(self):
        """Тестирование вывода списка уроков"""
        Lesson.objects.create(name='Тестовый урок', description='test lesson')
        response = self.client.get('/lesson/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [{'course_id': None,
                                           'description': 'test lesson',
                                           'id': 2, 'name': 'Тестовый урок',
                                           'owner': None, 'preview': None, 'url': None}])


    def test_retrieve_lesson(self):
        """Тест на просмотр урока"""
        Lesson.objects.create(name='детальный тест', description='test_detail')
        response = self.client.get('/lesson/3/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 3, 'name': 'детальный тест',
                                            'preview': None, 'description': 'test_detail',
                                            'url': None, 'course_id': None, 'owner': None})


    def test_update_lesson(self):
        """Тест  на изменение урока"""
        Lesson.objects.create(name='test_update', description='test_update')
        #Lesson.objects.update(owner=1)
        response = self.client.patch('/lesson/update/4/', data={'description': 'TEST UPDATE'})
        #print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'id': 4, 'name': 'test_update',
                                           'preview': None, 'description': 'TEST UPDATE',
                                           'url': None, 'course_id': None, 'owner': None})

    # def test_delete_lesson(self):
    #     """Тест на удаление урока"""
    #     Lesson.objects.create(name='test_del', description='test_del')
    #     response = self.client.delete('/lesson/delete/5/')
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
