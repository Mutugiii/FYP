from django.shortcuts import reverse
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from rest_framework import status

from ..models import Post
User = get_user_model()


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.valid_user_payload = {
            'username': 'test',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@test.com',
            'password': 'test2020',
            'bio': 'Just a test user',
            'location': 'Nairobi'
        }

        self.duplicate_user_payload = {
            'username': 'test',
            'password': 'test2020'
        }

        self.invalid_user_password_payload = {
            'username': 'testing',
            'password': 'test'
        }

        self.invalid_user_payload = {
            'email': 'test@test.com',
            'password': 'test2020',
        }

    def test_user_register(self):
        self.response = self.client.post(
            reverse('register'),
            data=self.valid_user_payload
        )

        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_missing_username(self):
        self.response = self.client.post(
            reverse('register'),
            data=self.invalid_user_payload
        )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        self.client.post(
            reverse('register'),
            data=self.valid_user_payload
        )
        self.response = self.client.post(
            reverse('register'),
            data=self.duplicate_user_payload
        )   
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_min_password(self):
        self.response = self.client.post(
            reverse('register'),
            data=self.invalid_user_password_payload
        )

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self):
        User.objects.all().delete()



class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client.post(
            reverse('register'),
            data= {
            'username': 'test',
            'password': 'test2020'
            }
        )
        
        self.valid_user_payload = {
            'username': 'test',
            'password': 'test2020'
        }
        self.invalid_user_payload = {
            'username': 'test',
            'password': 'test2000'
        }

    def test_login(self):
        self.response = self.client.post(
            reverse('login'),
            data=self.valid_user_payload
        )
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_login_invalid_data(self):
        self.response = self.client.post(
            reverse('login'),
            data=self.invalid_user_payload
        )
        self.assertEqual(self.response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def tearDown(self):
        User.objects.all().delete()

class GetPostPostView(TestCase):
    def setUp(self):
        self.client.post(
            reverse('register'),
            data= {
            'username': 'test',
            'password': 'test2020'
            }
        )

        self.res = self.client.post(
            reverse('login'),
            data = {
                'username': 'test',
                'password': 'test2020'
            }
        ).json()


    def test_get_all_posts(self):
        self.response = self.client.get(
            reverse('post_api')
        )
        
        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(len(self.response.json()) == 0)

    def test_create_valid_post(self):
        self.client = Client(HTTP_AUTHORIZATION=f'Bearer {self.res["authentication"]["access_token"]}')
        self.response = self.client.post(
            reverse('post_api'),
            data = {
                'title': 'Hello World',
                'about': 'Testing', 
                'user': self.res['user']['id']
            }
        )

        self.assertEqual(self.response.status_code, 201)
        self.assertTrue(self.response.json()['title'] == 'Hello World')

    def test_unauthorized_create_post(self):
        self.response = self.client.post(
            reverse('post_api'),
            data= {
                'title': 'Hello World',
                'about': 'Testing', 
                'user': self.res['user']['id']
            }
        )

        self.assertEqual(self.response.status_code, 401)
        self.assertTrue(self.response.json()["detail"] == "Authentication credentials were not provided.")
    
    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()

class GetPutDeletePostDetailsView(TestCase):
    def setUp(self):
        self.client.post(
            reverse('register'),
            data= {
            'username': 'test',
            'password': 'test2020'
            }
        )

        self.res = self.client.post(
            reverse('login'),
            data = {
                'username': 'test',
                'password': 'test2020'
            }
        ).json()

        self.client = Client(HTTP_AUTHORIZATION=f'Bearer {self.res["authentication"]["access_token"]}')
        self.post = self.client.post(
            reverse('post_api'),
            data = {
                'title': 'Hello World',
                'about': 'Testing', 
                'user': self.res['user']['id']
            }
        )

    def test_get_post(self):
        self.response = self.client.get(
            reverse('posts_api', kwargs={
                'id': self.post.json()['id']
            })
        )

        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.response.json() == self.post.json())

    def test_put_post(self):
        self.response = self.client.put(
            reverse('posts_api', kwargs={
                'id': self.post.json()['id']
            }),
            data = {
                'title': 'New Hello World',
                'about': 'Testing'
            },
            content_type='application/json'
        )

        self.assertEqual(self.response.status_code, 200)
        self.assertTrue(self.response.json()['title'] == 'New Hello World')
    
    def test_delete_post(self):
        self.response = self.client.delete(
            reverse('posts_api', kwargs={
                'id': self.post.json()['id']
            }),
        )
        self.assertEqual(self.response.status_code, 200)

    def tearDown(self):
        User.objects.all().delete()
        Post.objects.all().delete()