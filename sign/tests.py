from django.contrib.auth.models import User
from django.test import TestCase
from sign.models import Guest, Event


class ModelTest(TestCase):

    def setUp(self) -> None:
        Event.objects.create(id=1, name='sanxing Galaxy9', status=True, limit=2000,
                             address='shenzhen', start_time='2021-06-20 19:30:00')

        Guest.objects.create(id=1, event_id=1, realname='a lin ', phone='13929003400',
                             email='alin@email.com', sign=False)

    def test_event_models(self):
        result = Event.objects.get(name='sanxing Galaxy9')
        self.assertEqual(result.address, 'shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone='13929003400')
        self.assertEqual(result.realname, 'a lin ')
        self.assertFalse(result.sign)


class IndexPageTest(TestCase):
    '''测试登录首页index'''

    def test_index_page(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


class LoginTest(TestCase):

    def setUp(self) -> None:
        User.objects.create_user('hufeiliang', 'hufeiliang@163.com', 'hu1234')

    def test_add_user(self):
        ret = User.objects.get(username="hufeiliang")
        print(ret.username)
        self.assertEqual(ret.username, "hufeiliang")

    def test_login_passwordIsNull(self):
        test_data = {'username': 'hufeiliang', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertIn(b' username or password error !', response.content)

    def test_login_success(self):
        test_data = {"username": "hufeiliang", "password": "hu1234"}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 302)
