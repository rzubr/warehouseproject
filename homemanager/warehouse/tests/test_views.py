from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from warehouse.models import Home, Product, Category

        
# class TestHomeView(TestCase):

#     def setUp(self):
#         test_user = User.objects.create_user(username='testuser', password='password')
#         test_user.save()
#         self.home_url = reverse('warehouse:home')
#         Home.objects.create(name='test_home')
#         Home.objects.create(name='test_home2')
#         home = Home.objects.get(name='test_home')
#         home2 = Home.objects.get(name='test_home2')
#         home.client.add(test_user.client)

#     def test_not_logged_redirect(self):
#         response = self.client.get(self.home_url)
#         self.assertEquals(response.status_code, 302)

#     def test_logged_in(self):
#         login = self.client.login(username='testuser', password='password')
#         response = self.client.get(self.home_url)
#         self.assertEqual(str(response.context['user']), 'testuser')
#         self.assertEqual(response.status_code, 200)
#         #Check if logged user get his home
#         self.assertEqual(str(response.context['object_list'][0]), 'test_home')
#         #Check if logged user doesnt get not his home in response
#         home2 = Home.objects.get(name='test_home2')
#         self.assertFalse(home2 in response.context['object_list'])
#         #Check template
#         self.assertTemplateUsed(response, 'warehouse/home.html')
    

class TestCreateHomeView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_user.save()
        self.create_url = reverse('warehouse:create_home')

    def test_not_logged_redirect(self):
        client = Client()
        response = client.get(self.create_url)
        self.assertEquals(response.status_code, 302)

    def test_logged_user_post(self):
        login = self.client.login(username='testuser', password='password')
        #Ceck if get not allowed check
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 405)
        #Check if create view redirect after post request
        post_response = self.client.post(self.create_url, {
            'name': 'Home',
            'client': self.test_user.client
        })
        self.assertEqual(post_response.status_code, 302)
        #Check if home is created correctly
        home = Home.objects.get(name='Home')
        self.assertTrue(self.test_user.client in home.client.all())


class TestUpdateHomeView(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(username='testuser', password='password')
        self.test_user.save()
        self.test_home = Home.objects.create(
            name= 'home_to_update',
        )
        self.test_home.client.add(self.test_user.client)
        self.update_url = reverse('warehouse:update_home', args=[self.test_home.pk])

    def test_update_request(self):
        login = self.client.login(username='testuser', password='password')
        response = self.client.post(self.update_url, {
            'name': 'updated_home',
        })
        #Check redirect after post request
        self.test_home.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        #Check if name is changed
        self.assertTrue(self.test_home.name == 'updated_home')
        #Check if client has not been changed
        self.assertTrue(self.test_user.client in self.test_home.client.all())

# class TestUpdateHomeView(TestCase):
    
#     def test_not_logged_redirect(self):
#         client = Client()
#         response = client.get(reverse('warehouse:update_home', args=['1']))
#         self.assertEquals(response.status_code, 302)


# class TestDeleteHomeView(TestCase):
    
#     def setUp(self):
#         self.client = Client
#         Home.objects.create(
#             name='test home',
#             client = client
#         )

#     def test_not_logged_redirect(self):
#         client = Client()
#         response = client.get(reverse('warehouse:delete_home', args=['1']))
#         self.assertEquals(response.status_code, 302)