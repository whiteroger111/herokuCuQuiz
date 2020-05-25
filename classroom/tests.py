from django.test import TestCase, Client

from django.urls import reverse


class LoginPageTest(TestCase):
    fixtures = ["datas.json"]

    def setUp(self):
        self.client = Client()

    def test_login_page_returns_correct_html(self):
        loginurl = reverse('login')
        response = self.client.get(loginurl)
        self.assertEqual(response.status_code, 200)
        # test response contains Username and Password
        self.assertIn('მომხმარებელის სახელი', response.content)
        self.assertIn('პაროლი', response.content)

        # blank fields
        response = self.client.post(loginurl)
        self.assertIn('ეს ველი სავალდებულოა.', response.content)

        # wrong username or password
        response = self.client.post(loginurl, {'username': 'bad', 'password': 'bad'})
        self.assertIn('გთხოვთ ჩაწეროთ სწორი მომხმარებლის სახელი და პაროლი.', response.content)

    def test_login_as_teacher(self):
        loginurl = reverse('login')
        # login as teacher
        response = self.client.post(loginurl, {'username': 'sumee', 'password': 'sumee1910'}, follow=True)
        self.assertEqual(response.redirect_chain[1][0], reverse('teachers:quiz_change_list'))
        self.assertIn(b'My Quizzes', response.content)


