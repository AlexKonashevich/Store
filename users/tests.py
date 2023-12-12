from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.forms import EmailVerification, User


class UserRegistrationViewTestCase(TestCase):

    def setUp(self):
        self.data = {
            'first_name': 'Alex', 'last_name': 'Ivanov',
            'username': 'Alex123', 'email': 'dmswgoh@mail.ru',
            'password1': '12345678Aa', 'password2': '12345678Aa',
        }
        self.path = reverse('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post_success(self):

        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())
        response = self.client.post(self.path, self.data)

        # check creating of user
        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEquals(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)

    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertEquals(response.context_data['title'], 'Store - Авторизация')
        self.assertTemplateUsed(response, 'users/login.html')


class UserProfileViewTestCase(TestCase):

    pass
