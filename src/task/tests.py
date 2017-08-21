from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Task
from django.contrib.auth.models import User


class AccountTests(APITestCase):

    def test_get_list_task_api(self):
        user = User.objects.create(username='alex', password="1234567Q")

        for n in range(10):
            name = "task {number}".format(number=n)
            description = "task {number} description".format(number=n)
            Task.objects.create(name=name, description=description,
                                user_added=user)

        self.client.force_authenticate(user=user)
        url = reverse('task_api:list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Task.objects.all().count())

        data = {
            'limit': 5
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), data['limit'])

        data['done'] = False

        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), data['limit'])

        data['done'] = True
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        data = {
            'prev_id': 4,
        }
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

        for i, item in enumerate(response.data):
            assert item['id'] < data['prev_id']

    def test_add_task_api(self):
        user = User.objects.create(username='alex', password="1234567Q")
        self.client.force_authenticate(user=user)

        url = reverse('task_api:add')
        data ={
            'name': 'task name',
            'description' : 'task description',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task = Task.objects.all().first()
        self.assertEqual(Task.objects.all().count(), 1)
        self.assertEqual(task.name, data['name'])
        self.assertEqual(task.description, data['description'])

    def test_edit_task_api(self):
        user = User.objects.create(username='alex', password="1234567Q")
        self.client.force_authenticate(user=user)

        name = "NAME TASK"
        description = "DESCRIPTION TASK"
        task = Task.objects.create(name=name, description=description,
                                    user_added=user)

        url = reverse('task_api:edit', kwargs={'id': task.id})
        data = {
            'name': 'NEW NAME TASK',
            'description': 'NEW DESCRIPTION TASK'
        }
        response = self.client.put(url, data, format='json')
        task = Task.objects.all().first()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(task.name, data['name'])
        self.assertEqual(task.description, data['description'])

    def test_delete_task_api(self):
        user = User.objects.create(username='alex', password="1234567Q")
        self.client.force_authenticate(user=user)

        task = Task.objects.create(name="name", description="description",
                                    user_added=user)

        url = reverse('task_api:delete', kwargs={'id': task.id})
        response = self.client.delete(url, format='json')

        self.assertEqual(Task.objects.all().count(), 0)

    def test_done_undone_task_api(self):
        user = User.objects.create(username='alex', password="1234567Q")
        self.client.force_authenticate(user=user)

        task = Task.objects.create(name="name", description="description",
                                    user_added=user)

        url_done = reverse('task_api:done', kwargs={'id': task.id})
        url_undone = reverse('task_api:undone', kwargs={'id': task.id})

        response = self.client.put(url_done, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.all().first().is_done, True)

        response = self.client.put(url_undone, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Task.objects.all().first().is_done, False)
